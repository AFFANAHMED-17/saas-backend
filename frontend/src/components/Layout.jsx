import { Link, Outlet, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Layout() {
    const { user, logout } = useAuth();
    const location = useLocation();

    const navigation = [
        { name: 'Dashboard', href: '/dashboard' },
        { name: 'AI Studio', href: '/generate' },
        { name: 'Plans', href: '/plans' },
        { name: 'Invoices', href: '/invoices' },
        ...(user?.is_superuser ? [{ name: 'Admin', href: '/admin' }] : []),
    ];

    return (
        <div className="flex h-screen bg-gray-100">
            <div className="w-64 bg-white shadow-md">
                <div className="p-6">
                    <h1 className="text-2xl font-bold text-indigo-600">SaaS Billing</h1>
                </div>
                <nav className="mt-6 px-4 space-y-2">
                    {navigation.map((item) => (
                        <Link
                            key={item.name}
                            to={item.href}
                            className={`block px-4 py-2 rounded-md ${location.pathname === item.href
                                ? 'bg-indigo-50 text-indigo-700'
                                : 'text-gray-600 hover:bg-gray-50'
                                }`}
                        >
                            {item.name}
                        </Link>
                    ))}
                </nav>
            </div>

            <div className="flex-1 flex flex-col overflow-hidden">
                <header className="bg-white shadow">
                    <div className="flex justify-between items-center px-6 py-4">
                        <h2 className="text-xl font-semibold text-gray-800">
                            {navigation.find(i => i.href === location.pathname)?.name || 'Pro'}
                        </h2>
                        <div className="flex items-center gap-4">
                            <span className="text-sm text-gray-600">{user?.email}</span>
                            <button
                                onClick={logout}
                                className="text-sm text-red-600 hover:text-red-800"
                            >
                                Sign out
                            </button>
                        </div>
                    </div>
                </header>

                <main className="flex-1 overflow-auto p-6">
                    <Outlet />
                </main>
            </div>
        </div>
    );
}
