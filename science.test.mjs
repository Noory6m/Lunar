import assert from 'node:assert/strict';
import fs from 'node:fs';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
import {polarToGeo,geoToPolar,bodyPoint,basis,project,direction,sample,makeGrid,firstHit,triangleHit} from '../frontend/science.js';
const root=path.dirname(path.dirname(fileURLToPath(import.meta.url)));
for(const xy of [[-11000,-12000],[1000,30000],[-15000,8000]]){const g=polarToGeo(...xy),back=geoToPolar(g.lat,g.lon);assert.ok(Math.hypot(back[0]-xy[0],back[1]-xy[1])<1e-6);}
assert.equal(triangleHit([0,0,1],[0,0,-1],[-1,-1,0],[1,-1,0],[0,1,0]),1);
assert.equal(triangleHit([3,0,1],[0,0,-1],[-1,-1,0],[1,-1,0],[0,1,0]),null);
const get=n=>JSON.parse(fs.readFileSync(path.join(root,'frontend/assets',n)));
const local=get('mission-terrain.json'),regional=get('regional-terrain.json'),ephem=get('horizons-example.json');
const g=polarToGeo(-11000,-12000),ref=basis(g.lat,g.lon),origin=bodyPoint(g.lat,g.lon,0),o=ephem.observer,ground=sample(local,o.lat,o.lon),at=basis(o.lat,o.lon),observer=project(bodyPoint(o.lat,o.lon,ground+2),origin,ref),grids=[makeGrid(local,origin,ref),makeGrid(regional,origin,ref,local.bounds)];
assert.equal(firstHit(grids,observer,direction(0,90,at,ref)),null);
assert.ok(firstHit(grids,observer,direction(0,-45,at,ref)));
const check=(name,i)=>{const b=ephem[name][i];return firstHit(grids,observer,direction(b.az,b.el,at,ref));};
assert.equal(check('sun',0),null);assert.ok(check('earth',0));assert.equal(check('earth',168),null);
assert.ok(Math.abs((ground+2)/1000-o.altitudeKm)<1e-7);
const global=get('globe-dem.json');assert.equal(global.z.length,global.rows*global.cols);assert.equal(global.radiusM,1737400);assert.ok(global.z.some(z=>z<0)&&global.z.some(z=>z>0));
console.log('Coordinate round trips, 3D ray intersections, real Horizons cases, and globe dimensions passed.');
