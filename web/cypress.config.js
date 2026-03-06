const { defineConfig } = require("cypress");

module.exports = defineConfig({
    e2e: {
        baseUrl: 'http://apacheb5:80',
        supportFile: false,
        fixturesFolder: false,
        video: true,
        screenshotOnRunFailure: true
    },
});