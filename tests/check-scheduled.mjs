// Validate staged HTML as it will resolve from /blog/, plus shared footer coverage.
import assert from 'node:assert/strict';
import {readFileSync, readdirSync, existsSync} from 'node:fs';
import {resolve, dirname} from 'node:path';
import {fileURLToPath} from 'node:url';
const root=resolve(dirname(fileURLToPath(import.meta.url)),'..');
const read=p=>readFileSync(resolve(root,p),'utf8');
const posts=JSON.parse(read('docs/scheduled/manifest.json'));
assert.equal(posts.length,13);
const slugs=new Set(), dates=new Set(), paragraphs=new Set();
const required=['https://easytoolbox.io/','https://getfaloos.com/','https://play.google.com/store/apps/details?id=io.easytoolbox.app','https://play.google.com/store/apps/details?id=io.getfaloos.app','https://play.google.com/store/apps/details?id=com.usman.gamehouse'];
let footer=null;
function checkFooter(t,name){
 const block=t.match(/<!-- family-links:start -->([\s\S]*?)<!-- family-links:end -->/);
 assert.ok(block,name+': family footer missing');
 footer??=block[1];assert.equal(block[1],footer,name+': footer drift');
 for(const url of required)assert.ok(block[1].includes('href="'+url+'"'),name+': missing family link');
 assert.ok(block[1].includes('data-lang="ar"'));
 assert.ok(t.includes('href="/family.css?v=1"'));
}
for(const dir of ['.','ar','blog'])for(const f of readdirSync(resolve(root,dir)).filter(f=>f.endsWith('.html')))checkFooter(read(dir+'/'+f),dir+'/'+f);
for(const p of posts){
 assert.ok(!slugs.has(p.slug),'duplicate slug');slugs.add(p.slug);
 assert.ok(!dates.has(p.date),'duplicate date');dates.add(p.date);
 const day=new Date(p.date+'T12:00:00Z');
 assert.ok([1,3,5].includes(day.getUTCDay()));
 assert.ok(p.date>='2026-11-05'&&p.date<='2026-12-05');
 const t=read('docs/scheduled/'+p.slug+'.html');
 checkFooter(t,p.slug);
 assert.ok(t.includes('data-set-language="ar"')&&t.includes('src="/site-language.js"'));
 for(const lang of ['en','ar'])assert.ok(t.includes('<div data-lang="'+lang+'" lang="'+lang+'"'),p.slug+': article translation missing');
 assert.ok(t.includes('Sources reviewed 4 November 2026')&&t.includes('رُوجعت المصادر في 4 نوفمبر 2026'));
 assert.ok(t.includes('role="img"')&&t.includes('Original Gulfline Digital process diagram'));
 assert.ok(t.includes('ca-pub-1711571975132715')&&t.includes('GTM-588P5J29')&&t.includes('G-D6BXRT8FXQ'));
 assert.ok(t.includes('src="/construction-banner.js"')&&t.includes('class="wa-float"'));
 assert.ok(t.includes('https://gulflinedigital.com/blog/'+p.slug+'.html'));
 const schema=JSON.parse(t.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/)[1]);
 assert.deepEqual(schema.inLanguage,['en','ar']);assert.equal(schema.headline,p.title);
 let total=0;
 for(const [n,body] of [...t.matchAll(/<div data-lang="(en|ar)" lang="\1"[^>]*>([\s\S]*?)<section class="sources">/g)].entries()){
   const text=body[2].replace(/<figure>[\s\S]*?<\/figure>/g,'');
   const count=text.replace(/<[^>]+>/g,' ').match(/\S+/g).length;
   assert.equal(count,p['word_count_'+body[1]],p.slug+': stale word count');total+=count;
   assert.ok(count>=400,p.slug+': translation too short');
   for(const match of text.matchAll(/<p>([\s\S]*?)<\/p>/g)){
      assert.ok(!paragraphs.has(match[1]),p.slug+': repeated article paragraph');paragraphs.add(match[1]);
   }
 }
 assert.ok(total>=900&&total<=1500,p.slug+': bilingual article outside 900–1500 words');
 assert.equal(schema.wordCount,total);
 for(const m of t.matchAll(/(?:href|src)="([^"]+)"/g)){
   const link=m[1];if(/^(?:[a-z][a-z0-9+.-]*:|#)/i.test(link))continue;
   const path=link.split(/[?#]/)[0];
   const target=path.startsWith('/')?resolve(root,'.'+path):resolve(root,'blog',path);
   assert.ok(existsSync(target),p.slug+': broken publication link '+link);
 }
 // Staged posts must not appear in live discovery files until publication.
 if(!existsSync(resolve(root,'blog',p.slug+'.html')))for(const f of ['blog/index.html','blog/rss.xml','sitemap.xml'])assert.ok(!read(f).includes(p.slug+'.html'),f+': premature listing');
}
console.log('PASS scheduled content: 13 bilingual articles, dates, 900–1500 combined body words, unique paragraphs, publication links, metadata and all-page family footers');
