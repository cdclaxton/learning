const fs = require('fs');
const path = require('path');

function* walkSync(dir) {
    const directory = fs.opendirSync(dir);
    while(1) {
        let ret = directory.readSync();
        if (!ret) {
            break;
        }
        const entry = path.join(dir, ret.name);
        if (ret.isDirectory()) {
            yield* walkSync(entry);
        } else {
            if (path.extname(ret.name) === '.feature') {
                yield(entry);
            }
        }        
    }
}

const dir = "../cypress-cucumber/";
console.log(`Walking directory: ${dir}`);

for (const d of walkSync(dir)) {
    console.log(`Feature file: ${d}`);
}