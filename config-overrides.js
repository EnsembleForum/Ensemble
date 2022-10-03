const path = require('path');

module.exports = {
    paths: function (paths, env) {        
        paths.appIndexJs = path.resolve(__dirname, 'frontend/index.tsx');
        paths.appSrc = path.resolve(__dirname, 'frontend');
        return paths;
    },
}