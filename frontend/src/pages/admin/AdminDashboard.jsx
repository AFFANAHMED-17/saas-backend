import { Link } from 'react-router-dom';

export default function AdminDashboard() {
    return (
        <div className="p-6">
            <h1 className="text-2xl font-bold mb-6">Admin Dashboard</h1>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <Link to="/admin/users" className="block p-6 bg-white rounded shadow hover:bg-gray-50">
                    <h2 className="text-xl font-bold text-gray-900">Manage Users</h2>
                    <p className="mt-2 text-gray-600">View and remove registered users.</p>
                </Link>
                <Link to="/admin/plans" className="block p-6 bg-white rounded shadow hover:bg-gray-50">
                    <h2 className="text-xl font-bold text-gray-900">Manage Plans</h2>
                    <p className="mt-2 text-gray-600">Create new subscription plans or delete existing ones.</p>
                </Link>
            </div>
        </div>
    );
}
