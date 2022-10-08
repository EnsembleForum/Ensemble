module.exports = {
  /*presets: [
    ['@babel/preset-env', {targets: {node: 'current'}}],
    '@babel/preset-typescript',
  ],*/
  "preset": "ts-jest",
  "transform": {
      "^.+\\.ts?$": "ts-jest",
      "^.+\\.(js|jsx)$": "babel-jest"
  },
  "testEnvironment": "jsdom",
  "moduleFileExtensions": [
    "ts",
    "tsx",
    "js",
    "json"
  ],
  "setupFilesAfterEnv": [
    "<rootDir>/tests/frontend/setupTests.ts"
  ]
};