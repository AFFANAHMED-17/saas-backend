import { useAuth } from '../context/AuthContext';

export default function Dashboard() {
    const { user } = useAuth();

    return (
        <div className="p-6">
            <h1 className="text-2xl font-bold">Dashboard</h1>
            <p className="mt-4">Welcome back, {user?.email}!</p>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-6">
                <div className="bg-white p-6 rounded shadow">
                    <h3 className="text-lg font-medium">Current Plan</h3>
                    <p className="text-gray-500">
                        {user?.subscription && user.subscription.length > 0
                            ? user.subscription[0].plan.name
                            : "Free Tier"}
                    </p>
                </div>
                <div className="bg-white p-6 rounded shadow">
                    <h3 className="text-lg font-medium">Usage</h3>
                    <p className="text-gray-500">
                        0 / {user?.subscription && user.subscription.length > 0
                            ? user.subscription[0].plan.request_limit
                            : 1000} requests
                    </p>
                </div>
                <div className="bg-white p-6 rounded shadow">
                    <h3 className="text-lg font-medium">Next Invoice</h3>
                    <p className="text-gray-500">No pending invoices</p>
                </div>
            </div>
        </div>
    );
}
