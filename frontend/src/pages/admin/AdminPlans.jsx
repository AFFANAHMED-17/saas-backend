import { useEffect, useState } from 'react';
import api from '../../lib/axios';

export default function AdminPlans() {
    const [plans, setPlans] = useState([]);
    const [loading, setLoading] = useState(true);
    const [newPlan, setNewPlan] = useState({ name: '', price: '0', interval: 'monthly', description: '' });

    useEffect(() => {
        fetchPlans();
    }, []);

    const fetchPlans = () => {
        api.get('/api/plans').then(res => setPlans(res.data)).finally(() => setLoading(false));
    };

    const createPlan = async (e) => {
        e.preventDefault();
        try {
            const payload = {
                ...newPlan,
                price: parseInt(newPlan.price) // Send as cents
            };
            await api.post('/api/plans', payload);
            setNewPlan({ name: '', price: '0', interval: 'monthly', description: '' });
            fetchPlans();
        } catch (err) {
            alert('Failed to create plan');
        }
    };

    const deletePlan = async (id) => {
        if (!window.confirm('Delete this plan?')) return;
        try {
            await api.delete(`/api/plans/${id}`);
            setPlans(plans.filter(p => p.id !== id));
        } catch (err) {
            alert('Failed to delete plan');
        }
    };

    if (loading) return <div>Loading plans...</div>;

    return (
        <div>
            <h1 className="text-2xl font-bold mb-6">Manage Plans</h1>

            <div className="bg-white p-6 rounded shadow mb-8">
                <h2 className="text-lg font-bold mb-4">Create New Plan</h2>
                <form onSubmit={createPlan} className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <input
                        className="border p-2 rounded"
                        placeholder="Plan Name"
                        value={newPlan.name}
                        onChange={e => setNewPlan({ ...newPlan, name: e.target.value })}
                        required
                    />
                    <input
                        type="number"
                        className="border p-2 rounded"
                        placeholder="Price (in cents)"
                        value={newPlan.price}
                        onChange={e => setNewPlan({ ...newPlan, price: e.target.value })}
                        required
                    />
                    <select
                        className="border p-2 rounded"
                        value={newPlan.interval}
                        onChange={e => setNewPlan({ ...newPlan, interval: e.target.value })}
                    >
                        <option value="monthly">Monthly</option>
                        <option value="yearly">Yearly</option>
                    </select>
                    <input
                        className="border p-2 rounded"
                        placeholder="Description"
                        value={newPlan.description}
                        onChange={e => setNewPlan({ ...newPlan, description: e.target.value })}
                    />
                    <input
                        type="number"
                        className="border p-2 rounded"
                        placeholder="Request Limit (e.g., 1000)"
                        value={newPlan.request_limit || ''}
                        onChange={e => setNewPlan({ ...newPlan, request_limit: parseInt(e.target.value) })}
                    />
                    <button type="submit" className="bg-indigo-600 text-white p-2 rounded hover:bg-indigo-700 md:col-span-2">
                        Create Plan
                    </button>
                </form>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {plans.map(plan => (
                    <div key={plan.id} className="bg-white p-6 rounded shadow border border-gray-100 flex flex-col justify-between">
                        <div>
                            <h3 className="text-xl font-bold text-gray-900">{plan.name}</h3>
                            <p className="mt-2 text-2xl font-extrabold text-indigo-600">
                                ${(plan.price / 100).toFixed(2)}
                                <span className="text-base font-medium text-gray-500">/{plan.interval}</span>
                            </p>
                            <p className="mt-2 text-gray-500">{plan.description}</p>
                        </div>
                        <button
                            onClick={() => deletePlan(plan.id)}
                            className="mt-4 w-full bg-red-100 text-red-700 py-2 px-4 rounded hover:bg-red-200 transition"
                        >
                            Delete Plan
                        </button>
                    </div>
                ))}
            </div>
        </div>
    );
}
