import * as vscode from "vscode";
import { ChatPanel } from "./panel";

export function activate(context: vscode.ExtensionContext) {
    let disposable = vscode.commands.registerCommand("chatbox.open", () => {
        ChatPanel.createOrShow(context.extensionUri);
    });

    context.subscriptions.push(disposable);
}

export function deactivate() {}
