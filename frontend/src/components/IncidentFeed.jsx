import React, { useEffect, useState } from 'react';
import { AlertTriangle, ShieldCheck, Lock, RefreshCw, Terminal } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import api from '../api';

const IncidentFeed = () => {
    const [incidents, setIncidents] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const fetchIncidents = async () => {
        setLoading(true);
        try {
            const auth = await api.post('/auth/token', new URLSearchParams({
                username: 'admin', password: 'admin'
            }));
            const token = auth.data.access_token;

            const response = await api.get('/incident/all', {
                headers: { Authorization: `Bearer ${token}` }
            });
            setIncidents(response.data.reverse());
            setError(null);
        } catch (err) {
            setError("Backend Offline");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchIncidents();
        const interval = setInterval(fetchIncidents, 3000);
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="bg-slate-900/80 backdrop-blur-sm border border-slate-800 rounded-2xl flex flex-col h-[600px] shadow-xl overflow-hidden">
            <div className="p-5 border-b border-slate-800 bg-slate-900/90 flex justify-between items-center z-10">
                <h2 className="text-lg font-bold text-white flex items-center gap-2">
                    <Terminal size={18} className="text-red-500" /> Live Threat Feed
                </h2>
                <div className="flex items-center gap-2">
                    <span className="text-xs font-mono text-slate-500 px-2 py-1 bg-slate-800 rounded border border-slate-700">
                        {incidents.length} EVENTS
                    </span>
                    <button
                        onClick={fetchIncidents}
                        className="p-1.5 hover:bg-slate-800 rounded-lg text-slate-400 transition-colors"
                    >
                        <RefreshCw size={16} className={loading ? "animate-spin" : ""} />
                    </button>
                </div>
            </div>

            <div className="flex-1 overflow-y-auto p-4 space-y-3 scrollbar-thin scrollbar-track-slate-900 scrollbar-thumb-slate-700">
                {error ? (
                    <div className="h-full flex flex-col items-center justify-center text-rose-500 gap-2 opacity-50">
                        <AlertTriangle size={32} />
                        <span className="text-sm font-medium">{error}</span>
                    </div>
                ) : (
                    <AnimatePresence>
                        {incidents.length === 0 && !loading && (
                            <motion.div
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                className="text-slate-600 text-center py-20 text-sm font-mono"
                            >
                // WAITING FOR SIGNALS...
                            </motion.div>
                        )}
                        {incidents.map((inc) => (
                            <motion.div
                                key={inc.id}
                                initial={{ opacity: 0, x: 20 }}
                                animate={{ opacity: 1, x: 0 }}
                                exit={{ opacity: 0 }}
                                className="group bg-slate-950/50 p-4 rounded-xl border border-slate-800 hover:border-red-500/30 transition-all hover:bg-red-950/10 cursor-default relative overflow-hidden"
                            >
                                <div className="absolute left-0 top-0 bottom-0 w-1 bg-red-500/50 rounded-l-xl"></div>

                                <div className="flex justify-between items-start mb-3">
                                    <div className="flex items-center gap-2">
                                        <span className="px-2 py-0.5 bg-red-500/10 text-red-400 text-[10px] font-bold tracking-wider rounded border border-red-500/20">
                                            {inc.detected_label.toUpperCase()}
                                        </span>
                                        <span className="text-[10px] text-slate-500 font-mono">
                                            #{inc.id.toString().padStart(4, '0')}
                                        </span>
                                    </div>
                                    <span className="text-[10px] text-slate-500 font-mono">
                                        {new Date(inc.timestamp).toLocaleTimeString()}
                                    </span>
                                </div>

                                <div className="mb-4">
                                    <div className="flex justify-between items-end mb-1">
                                        <span className="text-xs text-slate-400 font-medium">Confidence Score</span>
                                        <span className="text-sm font-bold text-white">{(inc.confidence * 100).toFixed(1)}%</span>
                                    </div>
                                    <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden">
                                        <div
                                            className="h-full bg-gradient-to-r from-orange-500 to-red-500"
                                            style={{ width: `${inc.confidence * 100}%` }}
                                        ></div>
                                    </div>
                                </div>

                                <div className="flex items-center justify-between pt-3 border-t border-slate-800/50">
                                    <div className="flex items-center gap-1.5 text-[10px] text-slate-500 group-hover:text-slate-400">
                                        <Lock size={10} />
                                        <span className="font-mono tracking-tight">AES-256 ENCRYPTED</span>
                                    </div>
                                    <div className="flex items-center gap-1.5 text-[10px] text-emerald-500/80">
                                        <ShieldCheck size={10} />
                                        <span>BLOCKED</span>
                                    </div>
                                </div>
                            </motion.div>
                        ))}
                    </AnimatePresence>
                )}
            </div>
        </div>
    );
};

export default IncidentFeed;
