const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const {classify,failure}=require('../js/rail-status.js');
const now=Date.parse('2026-10-30T00:00:00Z');
assert.equal(classify({success:true,data:[]},now).kind,'empty');
assert.equal(classify({data:[{title:'Old',createdAt:'2026-06-13T12:00:00Z'}]},now).kind,'stale');
assert.equal(classify({data:[{title:'Unknown'}]},now).kind,'stale');
assert.equal(classify({data:[{title:'Future',updatedAt:'2030-01-01'}]},now).kind,'stale');
assert.equal(classify({success:true,data:[{id:4,title:'Fresh',updatedAt:'2026-10-29T23:00:00Z'}]},now).kind,'fresh');
assert.equal(classify({disruptions:[{title:'Legacy shape',createdAt:'2026-10-29T23:00:00Z'}]},now).kind,'fresh');
assert.throws(()=>classify({success:false,data:[]},now));
assert.throws(()=>classify({data:{}},now));
assert.equal(classify({data:[null,4,'bad',{}]},now).kind,'empty');
assert.equal(classify({data:[{id:'javascript:1',title:'X'}]},now).records[0].id,null);
assert.equal(failure(null).kind,'unavailable');
const old=classify({data:[{title:'Past',createdAt:'2020-01-01'}]},now);
assert.equal(failure(old).kind,'cached');assert.equal(failure(old).previous,old);
class El {constructor(){this.children=[];this.textContent='';this.listeners={};this.disabled=false;}appendChild(e){this.children.push(e);}replaceChildren(){this.children=[];}addEventListener(t,f){this.listeners[t]=f;}}
async function run(){
 const ids=Object.fromEntries(['check-feed','status-copy','feed-message','feed-timing','feed-records'].map(id=>[id,new El()]));
 ids['status-copy'].textContent=JSON.stringify(Object.fromEntries(['loading','empty','fresh','stale','cached','unavailable','retrieved','sourceDate','undated','history'].map(k=>[k,k])));
 let calls=0;let mode='fail';
 const w={document:{getElementById:id=>ids[id],createElement:()=>new El(),documentElement:{lang:'en'}},AbortController,setTimeout,clearTimeout,Date,fetch:async()=>{calls++;if(mode==='fail')throw Error('network');if(mode==='http')return {ok:false};if(mode==='invalid')return {ok:true,json:async()=>({x:1})};return {ok:true,json:async()=>({data:mode==='empty'?[]:[{id:1,title:'<img src=x onerror=bad()>',updatedAt:new Date().toISOString()}]})};}};
 vm.runInNewContext(fs.readFileSync(require.resolve('../js/rail-status.js'),'utf8'),{window:w,module:{exports:{}},AbortController,Date});
 assert.equal(calls,0,'does not poll/fetch on load');
 const click=ids['check-feed'].listeners.click;
 await click();assert.equal(ids['feed-message'].textContent,'unavailable');assert.equal(ids['check-feed'].disabled,false);
 mode='http';await click();assert.equal(ids['feed-message'].textContent,'unavailable');
 mode='invalid';await click();assert.equal(ids['feed-message'].textContent,'unavailable');
 mode='empty';await click();assert.equal(ids['feed-message'].textContent,'empty');
 mode='fresh';await click();assert.equal(ids['feed-message'].textContent,'fresh');assert.equal(ids['feed-records'].children[0].children[0].textContent,'<img src=x onerror=bad()>');
 mode='fail';await click();assert.equal(ids['feed-message'].textContent,'cached');assert.equal(ids['feed-records'].children.length,1);
 mode='fresh';await Promise.all([click(),click()]);assert.equal(ids['check-feed'].disabled,false);
 console.log('status logic and DOM: passed (empty/fail/HTTP/malformed/stale/undated/future/fresh/cache/text safety/repeat click/no autopoll)');
}
run().catch(e=>{console.error(e);process.exitCode=1});
