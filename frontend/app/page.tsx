"use client";

import { useEffect, useState } from 'react';
import { api, Agent } from '../lib/api';

export default function Dashboard() {
    const [agents, setAgents] = useState<Agent[]>([]);
    const [loading, setLoading] = useState(true);

    const fetchAgents = async () => {
        try {
            const data = await api.getAgents();
            setAgents(data);
        } catch (error) {
            console.error("Failed to fetch agents", error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchAgents();
        const interval = setInterval(fetchAgents, 2000); // Poll every 2s
        return () => clearInterval(interval);
    }, []);

    const handleInjectFault = async (agentId: string, fault: string) => {
        await api.injectFault(agentId, fault);
        fetchAgents();
    };

    const handleRecover = async (agentId: string) => {
        await api.recoverAgent(agentId);
        fetchAgents();
    };

    return (
        <div className="min-h-screen bg-gray-900 text-white p-8">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-blue-400">AgentOps Dashboard</h1>
                <p className="text-gray-400">Monitoring & Self-Healing for AI Agents</p>
            </header>

            {loading && <p>Loading agents...</p>}

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {agents.map((agent) => (
                    <div key={agent.agent_id} className={`p-6 rounded-xl border ${agent.status === 'HEALTHY' ? 'border-green-500/30 bg-green-900/10' :
                            agent.status === 'UNHEALTHY' ? 'border-red-500/30 bg-red-900/10' :
                                'border-yellow-500/30 bg-yellow-900/10'
                        }`}>
                        <div className="flex justify-between items-start mb-4">
                            <div>
                                <h2 className="text-xl font-semibold">{agent.service_name}</h2>
                                <p className="text-xs text-gray-500">{agent.agent_id}</p>
                            </div>
                            <span className={`px-3 py-1 rounded-full text-xs font-bold ${agent.status === 'HEALTHY' ? 'bg-green-500/20 text-green-400' :
                                    agent.status === 'UNHEALTHY' ? 'bg-red-500/20 text-red-400' :
                                        'bg-yellow-500/20 text-yellow-400'
                                }`}>
                                {agent.status}
                            </span>
                        </div>

                        <div className="space-y-2 mb-6">
                            <div className="flex justify-between text-sm">
                                <span className="text-gray-400">Latency</span>
                                <span>{agent.metrics.latency_ms.toFixed(0)} ms</span>
                            </div>
                            <div className="flex justify-between text-sm">
                                <span className="text-gray-400">Error Rate</span>
                                <span>{(agent.metrics.error_rate * 100).toFixed(1)}%</span>
                            </div>
                            <div className="flex justify-between text-sm">
                                <span className="text-gray-400">Active Faults</span>
                                <span className="text-red-400">{agent.active_faults.join(', ') || 'None'}</span>
                            </div>
                        </div>

                        <div className="flex gap-2">
                            <button
                                onClick={() => handleInjectFault(agent.agent_id, 'LATENCY')}
                                className="flex-1 px-3 py-2 bg-yellow-600/20 hover:bg-yellow-600/40 text-yellow-400 text-sm rounded transition"
                            >
                                Inject Latency
                            </button>
                            <button
                                onClick={() => handleInjectFault(agent.agent_id, 'ERROR')}
                                className="flex-1 px-3 py-2 bg-red-600/20 hover:bg-red-600/40 text-red-400 text-sm rounded transition"
                            >
                                Inject Error
                            </button>
                            <button
                                onClick={() => handleRecover(agent.agent_id)}
                                className="flex-1 px-3 py-2 bg-blue-600/20 hover:bg-blue-600/40 text-blue-400 text-sm rounded transition"
                            >
                                Recover
                            </button>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
