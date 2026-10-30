const fs=require('fs'), vm=require('vm'), assert=require('node:assert/strict');
const code=fs.readFileSync(require('path').join(__dirname,'../js/conversion-events.js'),'utf8');
function setup(gtag) {
 const handlers={}, win={location:{pathname:'/zh/'},gtag};
 const ctx={window:win,document:{documentElement:{lang:'zh'},addEventListener:(n,h)=>handlers[n]=h}};
 vm.runInNewContext(code,ctx);return {handlers,win,ctx};
}
let events=[];let s=setup((...args)=>events.push(args));
const event=(dataset,type='click',button=0)=>({type,button,target:{closest:()=>({dataset})}});
s.handlers.click(event({conversionEntry:'swiss-buy',conversionPlacement:'home-buying-guides',conversionLanguage:'zh'}));
assert.equal(events.length,1);assert.equal(events[0][1],'buying_guide_click');assert.equal(events[0][2].page_path,'/zh/');
s.handlers.click(event({conversionProduct:'swiss-travel-pass',conversionFamily:'swiss-buy',conversionSubid:'et_zh_swiss_buy_r1'}));
assert.equal(events[1][1],'affiliate_product_click');assert.equal(events[1][2].sub_id,'et_zh_swiss_buy_r1');
s.handlers.auxclick(event({conversionEntry:'swiss-buy'},'auxclick',2));assert.equal(events.length,2);
s.handlers.auxclick(event({conversionEntry:'swiss-buy'},'auxclick',1));assert.equal(events.length,3);
let previous=s.handlers.click;vm.runInNewContext(code,s.ctx);assert.equal(previous,s.handlers.click);
s.handlers.click({target:null});s.handlers.click({target:{closest:()=>null}});assert.equal(events.length,3);
s=setup(undefined);assert.doesNotThrow(()=>s.handlers.click(event({conversionEntry:'swiss-buy'})));
s=setup(()=>{throw Error('blocked')});assert.doesNotThrow(()=>s.handlers.click(event({conversionEntry:'swiss-buy'})));
assert.ok(!/localStorage|sessionStorage|document\.cookie|fetch\(/.test(code));
console.log('PASS: conversion click, affiliate metadata, middle-click, right-click exclusion, duplicate load, no-op, blocked analytics, no storage');

let grouped=[];s=setup((...a)=>grouped.push(a));s.handlers.click(event({conversionProduct:"swiss-travel-pass",conversionGroup:"swiss_content_expansion"}));assert.equal(grouped[0][2].content_group,"swiss_content_expansion");console.log("PASS: content expansion uses its own event group");
