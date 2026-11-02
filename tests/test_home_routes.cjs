const fs=require('fs'),vm=require('vm'),assert=require('node:assert/strict'),path=require('path');
const root=path.join(__dirname,'..');
function node(extra={}){return Object.assign({handlers:{},hidden:false,attrs:{},dataset:{},addEventListener(n,h){this.handlers[n]=h},setAttribute(k,v){this.attrs[k]=v},removeAttribute(k){delete this.attrs[k]},focus(){this.focused=true},scrollIntoView(){this.scrolled=true}},extra)}
for(const lang of ['en','zh','de','fr','es','it','ja','ko','pt']){
 const html=fs.readFileSync(path.join(root,lang,'index.html'),'utf8');
 const form=node({dataset:{}}), attrs=html.match(/<form id="route-form"[^>]*>/)[0];
 for(const [_,k,v] of attrs.matchAll(/data-([a-z-]+)="([^"]+)"/g))form.dataset[k.replace(/-([a-z])/g,(_,c)=>c.toUpperCase())]=v;
 const ids={'route-form':form};
 for(const id of ['route-status','route-error','empty-routes','route-filters','reset-routes','empty-reset','swap-route','routes','routes-title'])ids[id]=node();
 for(const id of ['origin','destination']){const opts=Object.fromEntries([...html.match(new RegExp('<select id="'+id+'"[\\s\\S]*?</select>'))[0].matchAll(/<option value="([^"]*)">([^<]+)<\/option>/g)].map(m=>[m[1],m[2]]));ids[id]=node({value:'',get selectedOptions(){return[{textContent:opts[this.value]}]}})}
 const cards=[...html.matchAll(/<article class="route-card"[\s\S]*?<\/article>/g)].map(m=>{const ds=Object.fromEntries([...m[0].matchAll(/data-(from|to|region)="([^"]+)"/g)].map(x=>[x[1],x[2]]));const d={open:false};return node({dataset:ds,querySelector:s=>d})});
 const filters=[...html.matchAll(/<button[^>]*data-region-filter="([^"]+)"/g)].map(m=>node({dataset:{regionFilter:m[1]}}));
 const presets=[...html.matchAll(/data-preset="([^"]+)"/g)].map(m=>node({dataset:{preset:m[1]}}));
 const details={open:false}; const document={documentElement:{lang},getElementById:id=>ids[id],querySelectorAll:s=>s=='.route-card'?cards:s=='[data-region-filter]'?filters:s=='[data-preset]'?presets:[],querySelector:s=>details,addEventListener(){}};
 const window={location:{hash:''},addEventListener(){}};
 const script=lang==='en'||lang==='zh'?'home-travel.js':'home-travel-localized.js';vm.runInNewContext(fs.readFileSync(path.join(root,'js',script),'utf8'),{document,window});
 const shown=()=>cards.filter(c=>!c.hidden), submit=()=>form.handlers.submit({preventDefault(){}}),click=id=>ids[id].handlers.click();
 assert.equal(shown().length,11);assert.equal(form.hidden,false);
 for(const c of cards){for(const [a,b] of [[c.dataset.from,c.dataset.to],[c.dataset.to,c.dataset.from]]){ids.origin.value=a;ids.destination.value=b;submit();assert.equal(shown().length,1);assert.equal(shown()[0],c);assert.equal(c.querySelector('details').open,true);assert.ok(ids['route-status'].textContent.includes('11'));}}
 ids.origin.value='vienna';ids.destination.value='budapest';click('swap-route');assert.equal(ids.origin.value,'budapest');submit();assert.equal(shown().length,1);
 ids.origin.value='milan';ids.destination.value='barcelona';submit();assert.equal(shown().length,0);assert.equal(ids['empty-routes'].hidden,false);click('empty-reset');assert.equal(shown().length,11);
 ids.origin.value='paris';ids.destination.value='paris';submit();assert.equal(ids['route-error'].hidden,false);assert.equal(ids.destination.attrs['aria-invalid'],'true');click('reset-routes');assert.equal(ids['route-error'].hidden,true);
 for(const f of filters){f.handlers.click();assert.equal(shown().length,f.dataset.regionFilter==='all'?11:cards.filter(c=>c.dataset.region===f.dataset.regionFilter).length)}
 for(const p of presets){p.handlers.click();assert.equal(shown().length,1)}click('reset-routes');assert.equal(shown().length,11);
 console.log('PASS route search: '+lang+' 11 routes, both directions, swap, no match, error, reset, regions and presets');
}
