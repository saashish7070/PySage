// import * as vscode from "vscode";
// import * as path from "path";

// export class ChatPanel {
//     public static currentPanel: ChatPanel | undefined;
//     private readonly panel: vscode.WebviewPanel;
//     private readonly extensionUri: vscode.Uri;

//     private constructor(extensionUri: vscode.Uri) {
//         this.extensionUri = extensionUri;
//         this.panel = vscode.window.createWebviewPanel(
//             "Pysage",
//             "Chat with AI",
//             vscode.ViewColumn.One,
//             { enableScripts: true }
//         );

//         this.panel.webview.html = this.getHtml();
//         this.panel.webview.onDidReceiveMessage(
//             (message) => this.handleMessage(message),
//             null
//         );
//     }

//     public static createOrShow(extensionUri: vscode.Uri) {
//         if (ChatPanel.currentPanel) {
//             ChatPanel.currentPanel.panel.reveal(vscode.ViewColumn.One);
//         } else {
//             ChatPanel.currentPanel = new ChatPanel(extensionUri);
//         }
//     }

//     private getHtml(): string {
//         return `<!DOCTYPE html>
//         <html lang="en">
//         <head>
//             <meta charset="UTF-8">
//             <meta name="viewport" content="width=device-width, initial-scale=1.0">
//             <title>Pysage</title>
//             <script>
//                 function sendMessage() {
//                     const input = document.getElementById("chatInput").value;
//                     vscode.postMessage({ type: "sendMessage", text: input });
//                     document.getElementById("chatInput").value = "";
//                 }
//                 window.addEventListener("message", event => {
//                     const response = event.data.text;
//                     document.getElementById("chatbox").innerHTML += "<p><b>Pysage:</b> " + response + "</p>";
//                 });
//             </script>
//         </head>
//         <body>
//             <div id="chatbox" style="height:300px; overflow-y:auto;"></div>
//             <input type="text" id="chatInput" placeholder="Type a message">
//             <button onclick="sendMessage()">Send</button>
//         </body>
//         </html>`;
//     }

//     private async handleMessage(message: any) {
//         if (message.type === "sendMessage") {
//             const response: any = await fetch("http://127.0.0.1:8000/chat", {
//                 method: "POST",
//                 headers: { "Content-Type": "application/json" },
//                 body: JSON.stringify({ message: message.text })
//             }).then(res => res.json());

//             this.panel.webview.postMessage({ text: response.response });
//         }
//     }
// }


import * as vscode from "vscode";
import * as path from "path";
import * as fs from "fs";

export class ChatPanel {
    public static currentPanel: ChatPanel | undefined;
    private readonly panel: vscode.WebviewPanel;
    private readonly extensionUri: vscode.Uri;

    private constructor(extensionUri: vscode.Uri) {
        this.extensionUri = extensionUri;
        this.panel = vscode.window.createWebviewPanel(
            "Pysage",
            "Chat with AI",
            vscode.ViewColumn.One,
            {
                enableScripts: true,
                localResourceRoots: [vscode.Uri.joinPath(extensionUri, "webview")],
            }
        );

        this.panel.webview.html = this.getWebviewContent();

        this.panel.webview.onDidReceiveMessage(
            (message) => this.handleMessage(message),
            null
        );

        this.panel.onDidDispose(() => (ChatPanel.currentPanel = undefined));
    }

    public static createOrShow(extensionUri: vscode.Uri) {
        if (ChatPanel.currentPanel) {
            ChatPanel.currentPanel.panel.reveal(vscode.ViewColumn.One);
        } else {
            ChatPanel.currentPanel = new ChatPanel(extensionUri);
        }
    }

    private getWebviewContent(): string {
        const webview = this.panel.webview;
        const webviewPath = vscode.Uri.joinPath(this.extensionUri, "webview");

        const scriptUri = webview.asWebviewUri(vscode.Uri.joinPath(webviewPath, "script.js"));
        const styleUri = webview.asWebviewUri(vscode.Uri.joinPath(webviewPath, "style.css"));
        
        const htmlPath = path.join(webviewPath.fsPath, "index.html");
        let html = fs.readFileSync(htmlPath, "utf-8");

        // Replace relative paths with Webview URIs
        html = html.replace('href="style.css"', `href="${styleUri}"`);
        html = html.replace('src="script.js"', `src="${scriptUri}"`);

        return html;
    }

    private async handleMessage(message: any) {
        if (message.type === "sendMessage") {
            try {
                const response: any = await fetch("http://127.0.0.1:8000/chat", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ message: message.text }),
                }).then(res => res.json());

                this.panel.webview.postMessage({ text: response.response });
            } catch (error) {
                this.panel.webview.postMessage({ text: "⚠️ Error connecting to the AI server." });
            }
        }
    }
}
