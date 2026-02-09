"use client";

/**
 * CLI Interface Page
 * Phase I Integration - Access CLI functionality from web interface
 * Author: Sharmeen Asif
 */

import { useState } from "react";
import { useRouter } from "next/navigation";
import { getStoredToken } from "@/lib/api-client";

export default function CLIPage() {
  const router = useRouter();
  const [output, setOutput] = useState<string[]>([
    "Welcome to Todo CLI Web Interface",
    "Type 'help' to see available commands",
    "",
  ]);
  const [command, setCommand] = useState("");
  const [isProcessing, setIsProcessing] = useState(false);

  const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

  const executeCommand = async (cmd: string) => {
    const trimmedCmd = cmd.trim();
    if (!trimmedCmd) return;

    // Add command to output
    setOutput((prev) => [...prev, `$ ${trimmedCmd}`, ""]);
    setCommand("");
    setIsProcessing(true);

    try {
      const parts = trimmedCmd.split(" ");
      const mainCmd = parts[0].toLowerCase();
      const args = parts.slice(1);

      let response = "";
      const token = getStoredToken();
      const authHeaders: Record<string, string> = token ? { Authorization: `Bearer ${token}` } : {};

      switch (mainCmd) {
        case "help":
          response = `Available Commands:
  list [--completed | --active]  - List all tasks
  add <title>                    - Add a new task
  complete <id>                  - Mark task as complete
  delete <id>                    - Delete a task
  clear                          - Clear terminal
  exit                           - Go back to Tasks page

Examples:
  list                  - Show all tasks
  list --active        - Show only active tasks
  add Buy groceries    - Add new task
  complete 1           - Complete task #1
  delete 2             - Delete task #2`;
          break;

        case "list":
          const filter = args[0];
          let filterParam = "";
          if (filter === "--completed") filterParam = "?completed=true";
          else if (filter === "--active") filterParam = "?completed=false";

          const listRes = await fetch(`${apiUrl}/api/tasks${filterParam}`, {
            headers: authHeaders,
          });

          if (!listRes.ok) {
            if (listRes.status === 401) {
              response = "Error: Not authenticated. Please sign in again.";
              setTimeout(() => router.push("/auth/signin"), 2000);
            } else {
              response = `Error: ${listRes.statusText}`;
            }
            break;
          }

          const tasks = await listRes.json();

          if (tasks.length === 0) {
            response = "No tasks found.";
          } else {
            response = `Found ${tasks.length} task(s):\n\n`;
            response += tasks
              .map(
                (task: any, idx: number) =>
                  `${idx + 1}. [${task.completed ? "✓" : " "}] ${task.title}${
                    task.description ? `\n   ${task.description}` : ""
                  }`
              )
              .join("\n");
          }
          break;

        case "add":
          if (args.length === 0) {
            response = "Error: Please provide a task title\nUsage: add <title>";
            break;
          }

          const title = args.join(" ");

          const addRes = await fetch(`${apiUrl}/api/tasks`, {
            method: "POST",
            headers: { "Content-Type": "application/json", ...authHeaders },
            body: JSON.stringify({ title, completed: false }),
          });

          if (!addRes.ok) {
            if (addRes.status === 401) {
              response = "Error: Not authenticated. Please sign in again.";
              setTimeout(() => router.push("/auth/signin"), 2000);
            } else {
              response = `Error: ${addRes.statusText}`;
            }
            break;
          }

          const newTask = await addRes.json();
          response = `✓ Task created: "${newTask.title}"\n  ID: ${newTask.id}`;
          break;

        case "complete":
          if (args.length === 0) {
            response = "Error: Please provide a task ID\nUsage: complete <id>";
            break;
          }

          const taskIndex = parseInt(args[0]) - 1;

          // Get all tasks to find the ID
          const tasksRes = await fetch(`${apiUrl}/api/tasks`, {
            headers: authHeaders,
          });

          if (!tasksRes.ok) {
            response = `Error: ${tasksRes.statusText}`;
            break;
          }

          const allTasks = await tasksRes.json();

          if (taskIndex < 0 || taskIndex >= allTasks.length) {
            response = `Error: Invalid task number. Valid range: 1-${allTasks.length}`;
            break;
          }

          const taskToComplete = allTasks[taskIndex];

          const completeRes = await fetch(
            `${apiUrl}/api/tasks/${taskToComplete.id}`,
            {
              method: "PATCH",
              headers: { "Content-Type": "application/json", ...authHeaders },
              body: JSON.stringify({ completed: true }),
            }
          );

          if (!completeRes.ok) {
            response = `Error: ${completeRes.statusText}`;
            break;
          }

          response = `✓ Marked task as complete: "${taskToComplete.title}"`;
          break;

        case "delete":
          if (args.length === 0) {
            response = "Error: Please provide a task ID\nUsage: delete <id>";
            break;
          }

          const deleteIndex = parseInt(args[0]) - 1;

          // Get all tasks to find the ID
          const delTasksRes = await fetch(`${apiUrl}/api/tasks`, {
            headers: authHeaders,
          });

          if (!delTasksRes.ok) {
            response = `Error: ${delTasksRes.statusText}`;
            break;
          }

          const delAllTasks = await delTasksRes.json();

          if (deleteIndex < 0 || deleteIndex >= delAllTasks.length) {
            response = `Error: Invalid task number. Valid range: 1-${delAllTasks.length}`;
            break;
          }

          const taskToDelete = delAllTasks[deleteIndex];

          const deleteRes = await fetch(
            `${apiUrl}/api/tasks/${taskToDelete.id}`,
            {
              method: "DELETE",
              headers: authHeaders,
            }
          );

          if (!deleteRes.ok) {
            response = `Error: ${deleteRes.statusText}`;
            break;
          }

          response = `✓ Deleted task: "${taskToDelete.title}"`;
          break;

        case "clear":
          setOutput([
            "Welcome to Todo CLI Web Interface",
            "Type 'help' to see available commands",
            "",
          ]);
          setIsProcessing(false);
          return;

        case "exit":
          router.push("/tasks");
          return;

        default:
          response = `Error: Unknown command '${mainCmd}'\nType 'help' for available commands`;
      }

      setOutput((prev) => [...prev, response, ""]);
    } catch (error) {
      setOutput((prev) => [
        ...prev,
        `Error: ${error instanceof Error ? error.message : "Unknown error"}`,
        "",
      ]);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!isProcessing && command.trim()) {
      executeCommand(command);
    }
  };

  return (
    <div className="min-h-screen bg-black text-green-400 font-mono p-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-4 flex items-center justify-between border-b border-green-900 pb-2">
          <div>
            <h1 className="text-xl font-bold">Todo CLI - Web Interface</h1>
            <p className="text-sm text-green-600">
              Phase I: Command-Line Interface (Web Version)
            </p>
          </div>
          <button
            onClick={() => router.push("/tasks")}
            className="px-4 py-2 bg-green-900 hover:bg-green-800 rounded text-sm"
          >
            Back to GUI
          </button>
        </div>

        {/* Terminal Output */}
        <div className="bg-gray-900 rounded-lg p-4 min-h-[500px] max-h-[600px] overflow-y-auto mb-4">
          {output.map((line, idx) => (
            <div key={idx} className="whitespace-pre-wrap">
              {line}
            </div>
          ))}
          {isProcessing && (
            <div className="flex items-center space-x-2">
              <div className="animate-pulse">Processing...</div>
            </div>
          )}
        </div>

        {/* Command Input */}
        <form onSubmit={handleSubmit} className="flex items-center space-x-2">
          <span className="text-green-600">$</span>
          <input
            type="text"
            value={command}
            onChange={(e) => setCommand(e.target.value)}
            disabled={isProcessing}
            className="flex-1 bg-gray-900 border border-green-900 rounded px-3 py-2 focus:outline-none focus:border-green-500 disabled:opacity-50"
            placeholder="Type a command (e.g., 'list', 'add Buy milk', 'help')..."
            autoFocus
          />
          <button
            type="submit"
            disabled={isProcessing || !command.trim()}
            className="px-6 py-2 bg-green-900 hover:bg-green-800 rounded disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Run
          </button>
        </form>

        {/* Quick Commands */}
        <div className="mt-4 flex flex-wrap gap-2">
          <span className="text-green-600 text-sm">Quick:</span>
          <button
            onClick={() => executeCommand("help")}
            disabled={isProcessing}
            className="px-3 py-1 bg-gray-800 hover:bg-gray-700 rounded text-sm disabled:opacity-50"
          >
            help
          </button>
          <button
            onClick={() => executeCommand("list")}
            disabled={isProcessing}
            className="px-3 py-1 bg-gray-800 hover:bg-gray-700 rounded text-sm disabled:opacity-50"
          >
            list
          </button>
          <button
            onClick={() => executeCommand("list --active")}
            disabled={isProcessing}
            className="px-3 py-1 bg-gray-800 hover:bg-gray-700 rounded text-sm disabled:opacity-50"
          >
            list --active
          </button>
          <button
            onClick={() => executeCommand("clear")}
            disabled={isProcessing}
            className="px-3 py-1 bg-gray-800 hover:bg-gray-700 rounded text-sm disabled:opacity-50"
          >
            clear
          </button>
        </div>

        {/* Info */}
        <div className="mt-6 text-green-600 text-sm border-t border-green-900 pt-4">
          <p>
            💡 This is a web-based interface for the Phase I CLI. Use commands
            like a terminal!
          </p>
          <p className="mt-1">
            Original CLI: <code className="bg-gray-900 px-2 py-1 rounded">cd cli && uv run todo --help</code>
          </p>
        </div>
      </div>
    </div>
  );
}
