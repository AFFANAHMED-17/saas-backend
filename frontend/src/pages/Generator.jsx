import { useState } from 'react';
import api from '../lib/axios';
import { useAuth } from '../context/AuthContext';

export default function Generator() {
    const { user, loading: authLoading } = useAuth();
    const [prompt, setPrompt] = useState('');
    const [generating, setGenerating] = useState(false);
    const [history, setHistory] = useState([]); // Array of { type: 'user' | 'ai', content: string | blobUrl }

    const handleGenerate = async (e) => {
        e.preventDefault();
        if (!prompt.trim()) return;

        // Add user prompt to history
        const newHistory = [...history, { type: 'user', content: prompt }];
        setHistory(newHistory);
        setGenerating(true);
        setPrompt('');

        try {
            const res = await api.post('/api/generate',
                null,
                {
                    params: { prompt },
                    responseType: 'blob'
                }
            );

            // Create URL for the image blob
            const imageUrl = URL.createObjectURL(res.data);
            setHistory([...newHistory, { type: 'ai', content: imageUrl }]);
        } catch (err) {
            console.error(err);
            let errorMsg = "Failed to generate image.";
            if (err.response && err.response.status === 403) {
                errorMsg = "Quota limit reached! Please upgrade your plan.";
            }
            setHistory([...newHistory, { type: 'error', content: errorMsg }]);
        } finally {
            setGenerating(false);
        }
    };

    if (authLoading) return <div>Loading...</div>;

    const limit = user?.subscription?.[0]?.plan?.request_limit || 1000;
    const usage = user?.subscription?.[0]?.usage_count || 0;

    return (
        <div className="flex flex-col h-full">
            <div className="p-6 bg-white shadow-sm border-b flex justify-between items-center">
                <h1 className="text-xl font-bold text-gray-800">AI Studio</h1>
                <div className="text-sm">
                    <span className="text-gray-500">Usage: </span>
                    <span className={`font-bold ${usage >= limit ? 'text-red-600' : 'text-green-600'}`}>
                        {usage} / {limit}
                    </span>
                    <span className="text-gray-500"> requests</span>
                </div>
            </div>

            <div className="flex-1 overflow-y-auto p-6 space-y-6 bg-gray-50">
                {history.length === 0 && (
                    <div className="text-center text-gray-400 mt-20">
                        <p className="text-xl">What would you like to create today?</p>
                        <p className="text-sm mt-2">Type a prompt below to start.</p>
                    </div>
                )}

                {history.map((msg, idx) => (
                    <div key={idx} className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}>
                        <div className={`max-w-xl rounded-lg p-4 shadow-sm ${msg.type === 'user'
                                ? 'bg-indigo-600 text-white'
                                : msg.type === 'error'
                                    ? 'bg-red-50 text-red-600 border border-red-200'
                                    : 'bg-white border border-gray-100'
                            }`}>
                            {msg.type === 'ai' ? (
                                <img src={msg.content} alt="Generated" className="rounded-lg w-full" />
                            ) : (
                                <p>{msg.content}</p>
                            )}
                        </div>
                    </div>
                ))}

                {generating && (
                    <div className="flex justify-start">
                        <div className="bg-white border border-gray-100 rounded-lg p-4 shadow-sm">
                            <div className="animate-pulse flex space-x-2 items-center">
                                <div className="h-2 w-2 bg-indigo-400 rounded-full"></div>
                                <div className="h-2 w-2 bg-indigo-400 rounded-full"></div>
                                <div className="h-2 w-2 bg-indigo-400 rounded-full"></div>
                                <span className="text-gray-400 text-sm ml-2">Dreaming...</span>
                            </div>
                        </div>
                    </div>
                )}
            </div>

            <div className="p-4 bg-white border-t">
                <form onSubmit={handleGenerate} className="flex gap-4">
                    <input
                        className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                        placeholder="A futuristic city with flying cars, cyberpunk style..."
                        value={prompt}
                        onChange={(e) => setPrompt(e.target.value)}
                        disabled={generating || usage >= limit}
                    />
                    <button
                        type="submit"
                        disabled={generating || usage >= limit}
                        className={`px-6 py-2 rounded-lg font-medium transition-colors ${generating || usage >= limit
                                ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                                : 'bg-indigo-600 text-white hover:bg-indigo-700'
                            }`}
                    >
                        Generate
                    </button>
                </form>
            </div>
        </div>
    );
}
