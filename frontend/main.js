const { app, BrowserWindow } = require("electron");

function createWindow() {

    const win = new BrowserWindow({

        width: 1600,
        height: 950,

        webPreferences: {

            nodeIntegration: true,

            contextIsolation: false,

            webSecurity: false
        },

        autoHideMenuBar: true,

        backgroundColor: "#020617"
    });

    win.loadFile("index.html");
}

app.whenReady().then(() => {

    createWindow();

});