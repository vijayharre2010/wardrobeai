import { PythonShell } from "python-shell";

export async function POST(req) {
  try {
    const { userDetails } = await req.json();

    let options = {
      mode: "text",
      pythonOptions: ["-u"], // unbuffered stdout
      args: [userDetails],   // pass user details to Python
    };

    const messages = await PythonShell.run("textgen.py", options);

    // Python prints JSON, so return that directly
    return new Response(messages.join(""), { status: 200 });
  } catch (error) {
    console.error("PythonShell Error:", error);
    return new Response(JSON.stringify({ error: "Failed to generate outfit" }), {
      status: 500,
    });
  }
}
