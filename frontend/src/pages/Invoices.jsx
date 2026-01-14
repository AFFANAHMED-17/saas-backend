import { useEffect, useState } from 'react';
import api from '../lib/axios';

export default function Invoices() {
    const [invoices, setInvoices] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        api.get('/api/invoices').then(res => {
            setInvoices(res.data);
            setLoading(false);
        }).catch(err => setLoading(false));
    }, []);

    const downloadInvoice = async (id) => {
        const res = await api.get(`/api/invoices/${id}/download`);
        const blob = new Blob([res.data.content], { type: 'text/plain' });
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', res.data.filename);
        document.body.appendChild(link);
        link.click();
        link.remove();
    };

    if (loading) return <div>Loading invoices...</div>;

    return (
        <div>
            <h1 className="text-2xl font-bold mb-6">Invoice History</h1>
            <div className="bg-white shadow overflow-hidden rounded-md">
                <ul className="divide-y divide-gray-200">
                    {invoices.map((invoice) => (
                        <li key={invoice.id} className="px-6 py-4 flex items-center justify-between">
                            <div>
                                <p className="text-sm font-medium text-gray-900">Invoice #{invoice.id}</p>
                                <p className="text-sm text-gray-500">
                                    {new Date(invoice.created_at).toLocaleDateString()}
                                </p>
                            </div>
                            <div className="flex items-center gap-4">
                                <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${invoice.status === 'paid' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                                    }`}>
                                    {invoice.status}
                                </span>
                                <span className="text-sm font-medium text-gray-900">
                                    ${(invoice.amount / 100).toFixed(2)}
                                </span>
                                <button
                                    onClick={() => downloadInvoice(invoice.id)}
                                    className="text-indigo-600 hover:text-indigo-900 text-sm"
                                >
                                    Download
                                </button>
                            </div>
                        </li>
                    ))}
                    {invoices.length === 0 && (
                        <li className="px-6 py-4 text-gray-500">No invoices found.</li>
                    )}
                </ul>
            </div>
        </div>
    );
}
