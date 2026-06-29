import { useState } from 'react';
import { Code2, Mic, MicOff, MessageSquare, AlertCircle, Loader2 } from 'lucide-react';
import axios from 'axios';

export default function Editor() {
  const [code, setCode] = useState(`# Write your python code here\n\ndef hello_world():\n    print("Hello from CodeMentor AI")\n\nhello_world()`);
  const [language, setLanguage] = useState('python');
  const [output, setOutput] = useState('');
  const [loading, setLoading] = useState(false);
  const [promptInput, setPromptInput] = useState('');

  // Voice recording state
  const [isRecording, setIsRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState<MediaRecorder | null>(null);

  const handleGenerateCode = async () => {
    if (!promptInput.trim()) return;
    setLoading(true);
    try {
      const response = await axios.post(`${import.meta.env.VITE_API_URL || 'http://localhost:5000'}/api/prompt-to-code`, 
        { prompt: promptInput, language },
        { withCredentials: true }
      );
      if (response.data.code) {
        setCode((prev) => prev + '\n\n# Generated code:\n' + response.data.code);
      }
      setOutput('Code generated successfully from prompt!');
      setPromptInput('');
    } catch (err: any) {
      setOutput('Error generating code: ' + (err.response?.data?.error || err.message));
    } finally {
      setLoading(false);
    }
  };

  const handleAction = async (action: string) => {
    if (!code.trim()) return;
    setLoading(true);
    try {
      const response = await axios.post(`${import.meta.env.VITE_API_URL || 'http://localhost:5000'}/api/${action}`, 
        { code, language },
        { withCredentials: true }
      );
      setOutput(response.data.result);
    } catch (err: any) {
      setOutput('Error processing request: ' + (err.response?.data?.error || err.message));
    } finally {
      setLoading(false);
    }
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });
      const chunks: BlobPart[] = [];

      recorder.ondataavailable = (e) => chunks.push(e.data);
      recorder.onstop = async () => {
        const audioBlob = new Blob(chunks, { type: 'audio/webm' });
        await processAudio(audioBlob);
        stream.getTracks().forEach(track => track.stop());
      };

      recorder.start();
      setMediaRecorder(recorder);
      setIsRecording(true);
    } catch (err) {
      alert("Microphone access denied or not available.");
    }
  };

  const stopRecording = () => {
    if (mediaRecorder && isRecording) {
      mediaRecorder.stop();
      setIsRecording(false);
    }
  };

  const processAudio = async (audioBlob: Blob) => {
    setLoading(true);
    const formData = new FormData();
    formData.append('audio', audioBlob, 'recording.webm');
    formData.append('language', language);

    try {
      const response = await axios.post(`${import.meta.env.VITE_API_URL || 'http://localhost:5000'}/api/speech-to-code`, formData, {
        withCredentials: true,
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      if (response.data.code) {
        setCode((prev) => prev + '\n\n# Generated from voice:\n' + response.data.code);
      }
      setOutput('Voice prompt understood: ' + response.data.prompt);
    } catch (err: any) {
      setOutput('Error processing voice: ' + (err.response?.data?.error || err.message));
    } finally {
      setLoading(false);
    }
  };

  const saveSnippet = async (withOutput = false) => {
    try {
      await axios.post(`${import.meta.env.VITE_API_URL || 'http://localhost:5000'}/save_snippet`, 
        { code, language, explanation: withOutput && output ? output : 'Saved from workspace' },
        { withCredentials: true }
      );
      alert('Snippet saved to profile!');
    } catch (err) {
      alert('Failed to save snippet.');
    }
  };

  return (
    <div className="container mx-auto px-4 py-8 max-w-7xl h-[calc(100vh-4rem)] flex flex-col">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className="p-3 bg-primary/20 rounded-xl">
            <Code2 className="w-8 h-8 text-primary" />
          </div>
          <div>
            <h1 className="text-3xl font-bold text-foreground">AI Workspace</h1>
            <p className="text-muted-foreground">Write, analyze, and generate code with AI.</p>
          </div>
        </div>
        
        <div className="flex items-center gap-4">
          <select
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
            className="bg-background border border-border rounded-lg px-4 py-2 focus:ring-2 focus:ring-primary outline-none"
          >
            <option value="python">Python</option>
            <option value="javascript">JavaScript</option>
            <option value="cpp">C++</option>
            <option value="java">Java</option>
          </select>
          <button 
            onClick={() => saveSnippet(false)}
            className="px-4 py-2 border border-primary/50 text-primary hover:bg-primary/10 rounded-lg font-medium transition-colors"
          >
            Save Snippet
          </button>
        </div>
      </div>

      <div className="flex-1 grid lg:grid-cols-2 gap-6 min-h-0">
        
        {/* Editor Area */}
        <div className="glass rounded-2xl overflow-hidden flex flex-col border border-border shadow-2xl">
          <textarea
            value={code}
            onChange={(e) => setCode(e.target.value)}
            className="flex-1 w-full bg-background/50 p-6 font-mono text-sm resize-none outline-none focus:bg-background/80 transition-colors"
            spellCheck={false}
          />
          
          <div className="p-4 bg-secondary/50 border-t border-border flex flex-col gap-3">
            <div className="flex gap-2">
              <input 
                type="text" 
                value={promptInput}
                onChange={(e) => setPromptInput(e.target.value)}
                onKeyDown={(e) => { if (e.key === 'Enter') handleGenerateCode(); }}
                placeholder="Ask AI to generate code..."
                className="flex-1 bg-background border border-border rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-primary outline-none transition-all"
              />
              <button 
                onClick={handleGenerateCode}
                className="px-4 py-2 bg-primary/20 text-primary hover:bg-primary/30 rounded-lg font-medium text-sm transition-colors whitespace-nowrap"
              >
                Generate
              </button>
            </div>

            <div className="flex flex-wrap gap-3 items-center justify-between">
              <div className="flex gap-2">
                <button onClick={() => handleAction('explain')} className="px-3 py-1.5 bg-background border border-border rounded-md text-sm hover:bg-accent hover:text-accent-foreground transition-colors">
                  Explain Code
                </button>
                <button onClick={() => handleAction('improve')} className="px-3 py-1.5 bg-background border border-border rounded-md text-sm hover:bg-accent hover:text-accent-foreground transition-colors">
                  Improve
                </button>
                <button onClick={() => handleAction('debug')} className="px-3 py-1.5 bg-background border border-border rounded-md text-sm hover:text-red-500 transition-colors">
                  Find Bugs
                </button>
              </div>
              
              <button
                onClick={isRecording ? stopRecording : startRecording}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all ${
                  isRecording 
                    ? 'bg-red-500/20 text-red-500 border border-red-500/50 animate-pulse' 
                    : 'bg-primary text-primary-foreground hover:bg-primary/90'
                }`}
              >
                {isRecording ? <MicOff className="w-4 h-4" /> : <Mic className="w-4 h-4" />}
                {isRecording ? 'Stop Recording' : 'Voice to Code'}
              </button>
            </div>
          </div>
        </div>

        {/* Output Area */}
        <div className="glass rounded-2xl flex flex-col border border-border shadow-2xl overflow-hidden">
          <div className="px-6 py-4 bg-secondary/50 border-b border-border flex justify-between items-center font-medium">
            <div className="flex items-center gap-2">
              <MessageSquare className="w-5 h-5 text-primary" />
              AI Assistant Output
            </div>
            {output && !loading && (
              <button 
                onClick={() => saveSnippet(true)}
                className="px-3 py-1.5 text-xs bg-primary/20 text-primary hover:bg-primary/30 rounded-lg font-medium transition-colors border border-primary/20"
              >
                Save with Output
              </button>
            )}
          </div>
          <div className="flex-1 p-6 overflow-auto bg-background/50">
            {loading ? (
              <div className="h-full flex flex-col items-center justify-center text-muted-foreground space-y-4 animate-pulse">
                <Loader2 className="w-8 h-8 animate-spin text-primary" />
                <p>Analyzing code with Gemini AI...</p>
              </div>
            ) : output ? (
              <pre className="whitespace-pre-wrap font-mono text-sm leading-relaxed text-foreground">
                {output}
              </pre>
            ) : (
              <div className="h-full flex flex-col items-center justify-center text-muted-foreground space-y-4 opacity-50">
                <AlertCircle className="w-12 h-12" />
                <p className="text-center max-w-sm">
                  Run an analysis or use voice-to-code to see the AI's feedback here.
                </p>
              </div>
            )}
          </div>
        </div>

      </div>
    </div>
  );
}
