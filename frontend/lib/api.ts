const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface Agent {
    agent_id: string;
    service_name: string;
    status: 'HEALTHY' | 'UNHEALTHY' | 'DEGRADED' | 'RECOVERING';
    last_heartbeat: string;
    metrics: {
        latency_ms: number;
        error_rate: number;
        cpu_usage: number;
        memory_usage: number;
    };
    active_faults: string[];
    config: {
        region: string;
        image: string;
        version: string;
    };
}

export const api = {
    getAgents: async (): Promise<Agent[]> => {
        const res = await fetch(`${API_URL}/api/v1/agents`);
        if (!res.ok) throw new Error('Failed to fetch agents');
        return res.json();
    },

    injectFault: async (agentId: string, faultType: string) => {
        const res = await fetch(`${API_URL}/api/v1/agents/${agentId}/fault`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ fault_type: faultType, duration_seconds: 60 }),
        });
        if (!res.ok) throw new Error('Failed to inject fault');
        return res.json();
    },

    recoverAgent: async (agentId: string) => {
        const res = await fetch(`${API_URL}/api/v1/agents/${agentId}/recover`, {
            method: 'POST',
        });
        if (!res.ok) throw new Error('Failed to recover agent');
        return res.json();
    },
};
