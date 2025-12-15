import React, { useState } from 'react';
import { Send, Zap, ShieldAlert, CheckCircle, AlertTriangle } from 'lucide-react';
import api from '../api';

const Simulator = () => {
    const [text, setText] = useState("");
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleInject = async (e) => {
        e.preventDefault();
        if (!text.trim()) return;

        setLoading(true);
        setResult(null);

        try {
            const response = await api.post('/debug/report', {
                text: text,
                agent_id: "web-simulator-01"
            });
            setResult(response.data);
            setText("");
        } catch (error) {
            console.error(error);
            const errorMessage = error.response?.data?.detail || error.message || "Failed to connect to backend.";
            setResult({ 
                status: "error", 
                message: errorMessage + (error.response ? ` (Status: ${error.response.status})` : "") 
            });
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="bg-slate-900/80 backdrop-blur-sm border border-slate-800 rounded-2xl p-6 shadow-xl">
            <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                <Zap className="text-yellow-400" /> Threat Simulator
            </h3>
            <p className="text-sm text-slate-400 mb-4">
                Test the detection engine by injecting a mock SMS message directly into the pipeline.
            </p>

            <form onSubmit={handleInject} className="flex gap-2">
                <input
                    type="text"
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    placeholder="Type a scam message (e.g. 'URGENT: Verify bank details')"
                    className="flex-1 bg-slate-950 border border-slate-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-blue-500 transition-colors"
                />
                <button
                    disabled={loading}
                    className="bg-blue-600 hover:bg-blue-500 text-white px-6 py-2 rounded-lg font-medium transition-colors flex items-center gap-2 disabled:opacity-50"
                >
                    {loading ? "Scanning..." : <>Send <Send size={18} /></>}
                </button>
            </form>

            {result && (
                <>
                    {result.status === "error" ? (
                        <div className="mt-4 p-4 rounded-lg border flex items-start gap-3 bg-red-900/20 border-red-900/50 text-red-200">
                            <AlertTriangle className="shrink-0" />
                            <div>
                                <p className="font-bold">Error</p>
                                <p className="text-sm opacity-80">{result.message}</p>
                            </div>
                        </div>
                    ) : (
                        <div className={`mt-4 p-4 rounded-lg border flex items-start gap-3 ${result.detected_label === "scam"
                            ? "bg-red-900/20 border-red-900/50 text-red-200"
                            : "bg-green-900/20 border-green-900/50 text-green-200"
                            }`}>
                            {result.detected_label === "scam" ? <ShieldAlert className="shrink-0" /> : <CheckCircle className="shrink-0" />}
                            <div>
                                <p className="font-bold">
                                    Analysis: {result.detected_label?.toUpperCase()}
                                </p>
                                <p className="text-xs opacity-80 mt-1">
                                    Confidence: {(result.confidence * 100).toFixed(1)}% | Incident ID: {result.id}
                                </p>
                            </div>
                        </div>
                    )}
                </>
            )}
        </div>
    );
};

export default Simulator;
