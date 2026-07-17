import { useNavigate } from 'react-router-dom'
import { useState, useEffect } from 'react'
import api from '../api'

interface JobApplication {
    id: number
    company: string
    role: string
    status: string
    date_applied: string
    location: string
    notes: string | null
    url: string | null
    date_updated: string
}

function Dashboard() {
    const navigate = useNavigate()
    const [application, setApplication] = useState<JobApplication[]>([])
    const [company, setCompany] = useState('')
    const [role, setRole] = useState('')
    const [status, setStatus] = useState('')
    const [date_applied, setDateApplied] = useState('')
    const [location, setLocation] = useState('')
    const [notes, setNotes] = useState('')
    const [url, setUrl] = useState('')
    const [error, setError] = useState('')
    const [editingId, setEditingId] = useState<number | null>(null)
    const [editForm, setEditForm] = useState<JobApplication | null>(null)
    const [loading, setLoading] = useState(true)
    const [search, setSearch] = useState('')
    const [showModal, setShowModal] = useState(false)


    useEffect(() => {
        const fetchApplications = async () => {
            try {
                const response = await api.get('/applications')
                setApplication(response.data)
            } catch (error) {
                console.error('Error fetching applications:', error)
            } finally {
                setLoading(false)
            }
        }
        fetchApplications()
    }, [])


    const handleLogout = () => {
        localStorage.removeItem('token')
        navigate('/login')
    }

    const handleAddApplication = async (e: React.FormEvent) => {
        e.preventDefault()
        try {
            const response = await api.post('/applications', { company, role, status, date_applied, location, notes, url })
            setApplication([...application, response.data])
            setCompany('')
            setRole('')
            setStatus('')
            setDateApplied('')
            setLocation('')
            setNotes('')
            setUrl('')
            setShowModal(false)
        } catch {
            setError('Invalid application')
        }
    }

    const handleDelete = async (id: number) => {
        try {
            await api.delete(`/applications/${id}`)
            setApplication(application.filter((app) => app.id !== id))
        } catch {
            setError('Failed to delete application')
        }
    }

    const handleEdit = (app: JobApplication) => {
        setEditingId(app.id)
        setEditForm(app)
    }

    const handleSave = async () => {
        try {
            // eslint-disable-next-line @typescript-eslint/no-unused-vars
            const { id, date_updated, ...updateData } = editForm!
            const response = await api.put(`/applications/${editingId}`, updateData)
            setApplication(application.map((app) => app.id === editingId ? response.data : app))
            setEditingId(null)
            setEditForm(null)
        } catch {
            setError('Failed to update application')
        }
        
    }

    const filtered = application.filter(app =>
        app.company.toLowerCase().includes(search.toLowerCase()) ||
        app.role.toLowerCase().includes(search.toLowerCase())
    )

    if (loading) {
        return <p>Loading...</p>
    } 
    


    return (
        <div className="min-h-screen bg-gray-100">
            <nav className="bg-white shadow px-6 py-4 flex justify-between items-center">
                <h1 className="text-xl font-bold">PipelinePal</h1>
                <div className="flex gap-3">
                    <button onClick={() => setShowModal(true)} className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">Add Application</button>
                    <button onClick={handleLogout} className="bg-gray-200 text-gray-700 px-4 py-2 rounded hover:bg-gray-300">Logout</button>
                </div>
            </nav>
            {showModal && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
                    <div className="bg-white p-8 rounded-lg w-full max-w-lg">
                        <h2 className="text-xl font-bold mb-4">Add Application</h2>
                        <form className="flex flex-col gap-3" onSubmit={handleAddApplication}>
                            <input className="border border-gray-300 rounded px-3 py-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500"
                                type='text'
                                placeholder='Company'
                                value={company}
                                onChange={(e) => setCompany(e.target.value)}
                            />
                            <input className="border border-gray-300 rounded px-3 py-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500"
                                type='text'
                                placeholder='Role'
                                value={role}
                                onChange={(e) => setRole(e.target.value)}
                            />
                            <input className="border border-gray-300 rounded px-3 py-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500"
                                type='text'
                                placeholder='Status'
                                value={status}
                                onChange={(e) => setStatus(e.target.value)}
                            />
                            <input className="border border-gray-300 rounded px-3 py-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500"
                                type='text'
                                placeholder='Date Applied'
                                value={date_applied}
                                onChange={(e) => setDateApplied(e.target.value)}
                            />
                            <input className="border border-gray-300 rounded px-3 py-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500"
                                type='text'
                                placeholder='Location'
                                value={location}
                                onChange={(e) => setLocation(e.target.value)}
                            />
                            <input className="border border-gray-300 rounded px-3 py-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500"
                                type='text'
                                placeholder='Notes'
                                value={notes}
                                onChange={(e) => setNotes(e.target.value)}
                            />
                            <input className="border border-gray-300 rounded px-3 py-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500"
                                type='text'
                                placeholder='URL'
                                value={url}
                                onChange={(e) => setUrl(e.target.value)}
                            />
                            <button type='submit' className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600">Add Application</button>
                            <button type='button' onClick={() => setShowModal(false)} className="w-full bg-gray-200 text-gray-700 py-2 rounded hover:bg-gray-300">Cancel</button>
                        </form>
                    </div>
            </div>
            )}
            
            <main className="max-w-5xl mx-auto px-6 py-8">
                <input className="w-full border border-gray-300 rounded px-3 py-2 mb-6 focus:outline-none focus:ring-2 focus:ring-blue-500"
                type='text'
                placeholder='Search by company or role...'
                value={search}
                onChange={(e) => setSearch(e.target.value)}
            /> 


            {filtered.length === 0 && application.length === 0
                ? <p>No applications yet.</p>
                : filtered.length === 0
                ? <p>No results found.</p>
                : <div className="space-y-3">
                    {filtered.map((app: JobApplication) => (
                        app.id === editingId ? (
                            <div key={app.id} className="bg-white rounded-lg shadow p-4">
                                <div className="flex flex-col gap-3">
                                    <input className="border border-gray-300 rounded px-3 py-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500" value={editForm?.company || ''} onChange={(e) => setEditForm({...editForm!, company: e.target.value})} />
                                    <input className="border border-gray-300 rounded px-3 py-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500" value={editForm?.role || ''} onChange={(e) => setEditForm({...editForm!, role: e.target.value})} />
                                    <input className="border border-gray-300 rounded px-3 py-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500" value={editForm?.status || ''} onChange={(e) => setEditForm({...editForm!, status: e.target.value})} />
                                    <input className="border border-gray-300 rounded px-3 py-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500" value={editForm?.date_applied || ''} onChange={(e) => setEditForm({...editForm!, date_applied: e.target.value})} />
                                    <input className="border border-gray-300 rounded px-3 py-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500" value={editForm?.location || ''} onChange={(e) => setEditForm({...editForm!, location: e.target.value})} />
                                    <input className="border border-gray-300 rounded px-3 py-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500" value={editForm?.notes || ''} onChange={(e) => setEditForm({...editForm!, notes: e.target.value})} />
                                    <input className="border border-gray-300 rounded px-3 py-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500" value={editForm?.url || ''} onChange={(e) => setEditForm({...editForm!, url: e.target.value})} />
                                </div>
                                <div className="flex gap-2 mt-4">
                                    <button onClick={handleSave} className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">Save</button>
                                    <button onClick={() => { setEditingId(null); setEditForm(null) }} className="bg-gray-200 text-gray-700 px-4 py-2 rounded hover:bg-gray-300">Cancel</button>
                                </div>
                            </div>
                        ) : (
                            <div key={app.id} className="bg-white rounded-lg shadow p-4 flex justify-between items-center">
                                <div>
                                    <p className="font-semibold text-lg">{app.company}</p>
                                    <p className="text-gray-600">{app.role}</p>
                                    <p className="text-sm text-gray-400">{app.location} · {app.date_applied}</p>
                                </div>
                            <div className="flex items-center gap-2">
                                <span className="bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-sm">{app.status}</span>
                                <button onClick={() => handleEdit(app)} className="text-gray-500 hover:text-blue-500 px-2">Edit</button>
                                <button onClick={() => handleDelete(app.id)} className="text-gray-500 hover:text-red-500 px-2">Delete</button>
                            </div>
                        </div>
                        )
                        
                    ))}
            </div>}
            {error && <p>{error}</p>}
            </main>
            
            
        </div>
    )
}

export default Dashboard

