import { useState } from 'react'
import api from '../api'
import { useNavigate, Link } from 'react-router-dom'

function Login() {
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [error, setError] = useState('')
    const navigate = useNavigate()


    const handleSubmit = async (e:React.FormEvent) => {
        e.preventDefault()
        
        try{ 
            const response = await api.post('/login', { email, password})
            localStorage.setItem('token', response.data.token)
            navigate('/dashboard')
        } catch  {
            setError('Invalid email or password')
        }
        

    }

    return (
        <div className="min-h-screen bg-gray-100 flex items-center justify-center">
            <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
                <h1 className="text-2xl font-bold text-center mb-2">PipelinePal</h1>
                <p className="text-gray-500 text-center mb-6">Track your job search</p>
                <form className="flex flex-col gap-3" onSubmit={handleSubmit}>
                    <input className="border border-gray-300 rounded px-3 py-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500"
                        type='email'
                        placeholder='Email'
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />
                    <input className="border border-gray-300 rounded px-3 py-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500"
                        type='password'
                        placeholder='Password'
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                    {error && <p>{error}</p>}
                    <button className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600" type='submit'>Login</button>
                    
                </form>
                <Link to='/register' className="block text-center text-sm text-blue-500 hover:underline mt-4">Don't have an account? Register</Link>
            </div>
        </div>

        
    )
}


export default Login