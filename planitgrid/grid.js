const inD =['\'le\'',4,8,9,1,6,10,12,11,9];
const inL = [0,0,2,1,1,0,0,1,0];

const l = document.querySelectorAll('.L-item');
const lor = "RMCGBKSDV";
l.forEach((item, index) => {
    o = inL[index]
    if (o > 0){
        if (o>1){item.textContent = lor[index] + `(${o})`; }
        else { item.textContent = lor[index];}
    }
});

const h = document.querySelectorAll('.grid-item');
const pl = "lkvdcmrgsb";
const grid = [4,8,12,16,15,14,13,9,5,1,2,3];

const d = new Map();
let k = grid[0];
let v = inD[0];
d.set(k,v);
const factor = new Set();
factor.add(1)

for (let i = 1; i < 10; i++){
    let house = inD[i]
    let k = grid[house-1]
    let v = pl[i]
    if (factor.has(house)){
        v = d.get(k) + v;
    } else{
        factor.add(house);
    }
    d.set(k,v)
}

h.forEach((item, index) => {
    if (d.has(index+1)){ item.textContent = d.get(index+1);}
    });
