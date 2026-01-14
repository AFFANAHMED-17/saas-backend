import { useEffect, useState } from 'react';
import api from '../lib/axios';

export default function Plans() {
    const [plans, setPlans] = useState([]);
    const [loading, setLoading] = useState(true);
    const [message, setMessage] = useState('');

    useEffect(() => {
        api.get('/api/plans').then(res => {
            setPlans(res.data);
            setLoading(false);
        }).catch(err => setLoading(false));
    }, []);

    const subscribe = async (planId) => {
        try {
            await api.post('/api/subscribe', { plan_id: planId });
            setMessage('Subscribed successfully!');
        } catch (err) {
            setMessage(err.response?.data?.detail || 'Subscription failed');
        }
    };

    if (loading) return <div>Loading plans...</div>;

    return (
        <div>
            <h1 className="text-2xl font-bold mb-6">Available Plans</h1>
            {message && <div className="mb-4 p-4 bg-blue-100 text-blue-700 rounded">{message}</div>}

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {plans.map(plan => (
                    <div key={plan.id} className="bg-white p-6 rounded shadow border border-gray-100">
                        <h3 className="text-xl font-bold text-gray-900">{plan.name}</h3>
                        <p className="mt-2 text-3xl font-extrabold text-indigo-600">
                            ${(plan.price / 100).toFixed(2)}
                            <span className="text-base font-medium text-gray-500">/{plan.interval}</span>
                        </p>
                        <p className="mt-4 text-gray-500">{plan.description || "Unlock premium features."}</p>
                        <button
                            onClick={() => subscribe(plan.id)}
                            className="mt-8 w-full bg-indigo-600 text-white py-2 px-4 rounded hover:bg-indigo-700 transition"
                        >
                            Subscribe
                        </button>
                    </div>
                ))}
                {plans.length === 0 && <p>No plans available. Ask admin to create some.</p>}
            </div>
        </div>
    );
}
