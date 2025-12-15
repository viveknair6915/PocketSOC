import React, { useEffect, useState } from 'react';
import ArchitectureView from './ArchitectureView';
import IncidentFeed from './IncidentFeed';
import Simulator from './Simulator';
import { Activity, Radio, Wifi, Shield } from 'lucide-react';
import api from '../api';

const Dashboard = () => {
    const [stats, setStats] = useState({ backend: 'Connecting...', latency: '...' });

    useEffect(() => {
        const checkHealth = async () => {
            try {
                const start = Date.now();
                await api.get('/health');
                const end = Date.now();
                setStats({ backend: 'Online', latency: `${end - start}ms` });
            } catch (e) {
                setStats({ backend: 'Offline', latency: '-' });
            }
        };
        checkHealth();
        const i = setInterval(checkHealth, 5000);
        return () => clearInterval(i);
    }, []);

    return (
        <div className="min-h-screen bg-[#0B1120] text-slate-200 font-sans selection:bg-blue-500/30">
            {/* Navbar */}
            <nav className="bg-slate-900/50 backdrop-blur-lg border-b border-slate-800 sticky top-0 z-50">
                <div className="max-w-7xl mx-auto px-6 h-20 flex justify-between items-center">
                    <div className="flex items-center gap-3">
                        <div className="p-2 bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg shadow-lg shadow-blue-500/20">
                            <Shield className="text-white" size={24} />
                        </div>
                        <div>
                            <h1 className="text-2xl font-bold text-white tracking-tight">PocketSOC</h1>
                            <p className="text-xs text-blue-400 font-medium tracking-wider">THREAT INTELLIGENCE PLATFORM</p>
                        </div>
                    </div>

                    <div className="flex gap-4 items-center">
                        <div className={`px-4 py-1.5 rounded-full border flex items-center gap-2.5 text-sm font-medium transition-colors ${stats.backend === 'Online'
                            ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400'
                            : 'bg-rose-500/10 border-rose-500/20 text-rose-400'
                            }`}>
                            <span className={`relative flex h-2 w-2`}>
                                <span className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${stats.backend === 'Online' ? 'bg-emerald-400' : 'bg-rose-400'}`}></span>
                                <span className={`relative inline-flex rounded-full h-2 w-2 ${stats.backend === 'Online' ? 'bg-emerald-500' : 'bg-rose-500'}`}></span>
                            </span>
                            {stats.backend}
                        </div>

                        <div className="px-4 py-1.5 rounded-full bg-slate-800/50 border border-slate-700 text-slate-400 text-sm font-mono flex items-center gap-2">
                            <Activity size={14} /> {stats.latency}
                        </div>
                    </div>
                </div>
            </nav>

            {/* Main Content */}
            <main className="max-w-7xl mx-auto px-6 py-10 grid grid-cols-1 lg:grid-cols-3 gap-8">

                {/* Left Column */}
                <div className="lg:col-span-2 space-y-8">
                    <div className="space-y-8">
                        <ArchitectureView />
                        <Simulator />
                    </div>

                    {/* Info Card */}
                    <div className="bg-slate-900/50 border border-slate-800 rounded-2xl p-8 relative overflow-hidden group hover:border-slate-700 transition-colors">
                        <div className="absolute -right-10 -top-10 w-40 h-40 bg-blue-600/10 rounded-full blur-3xl group-hover:bg-blue-600/20 transition-all"></div>

                        <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                            <Radio className="text-blue-400" /> Operational Logic
                        </h3>
                        <div className="grid md:grid-cols-2 gap-6 text-sm text-slate-400">
                            <div className="space-y-3">
                                <p className="flex gap-2">
                                    <span className="text-blue-400 font-bold">01.</span>
                                    <span>Agent intercepts SMS and processes text via local <strong>TFLite CNN model</strong>.</span>
                                </p>
                                <p className="flex gap-2">
                                    <span className="text-blue-400 font-bold">02.</span>
                                    <span>If confidence &gt; 50%, payload is <strong>AES-256 encrypted</strong> on device.</span>
                                </p>
                            </div>
                            <div className="space-y-3">
                                <p className="flex gap-2">
                                    <span className="text-blue-400 font-bold">03.</span>
                                    <span>Secure POST request sent to FastAPI backend with <strong>JWT Auth</strong>.</span>
                                </p>
                                <p className="flex gap-2">
                                    <span className="text-blue-400 font-bold">04.</span>
                                    <span>Incident logged in <strong>Hash-Chained Audit Ledger</strong>.</span>
                                </p>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Right Column */}
                <div className="lg:col-span-1">
                    <IncidentFeed />
                </div>
            </main>
        </div>
    );
};

export default Dashboard;
