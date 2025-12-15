import React from 'react';
import { motion } from 'framer-motion';
import { Smartphone, Server, Database, ShieldAlert, Cpu, ArrowRight } from 'lucide-react';

const FlowArrow = ({ delay }) => (
    <motion.div
        initial={{ opacity: 0, x: -10 }}
        animate={{ opacity: [0, 1, 0], x: [0, 30, 60] }}
        transition={{ duration: 2, repeat: Infinity, delay: delay }}
        className="text-cyan-500 hidden md:block"
    >
        <ArrowRight size={24} strokeWidth={3} />
    </motion.div>
);

const Node = ({ icon: Icon, title, subtitle, color, borderColor, glowColor }) => (
    <motion.div
        whileHover={{ scale: 1.05 }}
        className="flex flex-col items-center gap-3 text-center z-10 relative group"
    >
        <div className={`p-6 bg-slate-800/80 backdrop-blur-md rounded-2xl border-2 ${borderColor} shadow-[0_0_20px_${glowColor}] transition-all duration-300 group-hover:shadow-[0_0_35px_${glowColor}]`}>
            <Icon size={40} className={color} />
        </div>
        <div className="flex flex-col">
            <span className="font-bold text-white tracking-wide">{title}</span>
            <span className="text-xs text-slate-400 font-mono uppercase tracking-wider">{subtitle}</span>
        </div>
    </motion.div>
);

const ArchitectureView = () => {
    return (
        <div className="bg-slate-900/50 p-8 rounded-2xl border border-slate-700/50 backdrop-blur-xl shadow-2xl relative overflow-hidden">
            {/* Background Gradients */}
            <div className="absolute top-0 left-0 w-full h-full bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-blue-900/20 via-transparent to-transparent pointer-events-none" />

            <h2 className="text-2xl font-bold mb-10 flex items-center gap-3 text-white">
                <Cpu className="text-purple-400" />
                <span className="bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400">
                    Live System Architecture
                </span>
            </h2>

            <div className="flex flex-col md:flex-row items-center justify-between gap-6 relative">
                {/* Connecting Line (Mobile only) */}
                <div className="absolute left-1/2 top-0 bottom-0 w-1 bg-slate-700/50 -translate-x-1/2 md:hidden"></div>
                {/* Connecting Line (Desktop) */}
                <div className="absolute top-1/2 left-0 right-0 h-1 bg-slate-700/50 -translate-y-1/2 hidden md:block"></div>

                <Node
                    icon={Smartphone} title="Mobile Agent" subtitle="TFLite Logic"
                    color="text-blue-400" borderColor="border-blue-500/50" glowColor="rgba(59,130,246,0.3)"
                />

                <FlowArrow delay={0} />

                <Node
                    icon={ShieldAlert} title="Detection" subtitle="On-Device AI"
                    color="text-yellow-400" borderColor="border-yellow-500/50" glowColor="rgba(234,179,8,0.3)"
                />

                <FlowArrow delay={0.6} />

                <Node
                    icon={Server} title="Secure Backend" subtitle="FastAPI + JWT"
                    color="text-green-400" borderColor="border-green-500/50" glowColor="rgba(74,222,128,0.3)"
                />

                <FlowArrow delay={1.2} />

                <Node
                    icon={Database} title="Audit Store" subtitle="Encrypted Logs"
                    color="text-indigo-400" borderColor="border-indigo-500/50" glowColor="rgba(99,102,241,0.3)"
                />

            </div>
        </div>
    );
};

export default ArchitectureView;
