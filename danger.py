import React, { useState } from 'react';
import { AlertCircle, Shield } from 'lucide-react';

const JWT_SECRET = '123456';

function createToken(user) {
  const data = btoa(JSON.stringify({ id: user.id, role: user.role }));
  return `token_${data}`;
}

export default function VulnerableApp() {
  const [user, setUser] = useState(null);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [tab, setTab] = useState('login');
  const [profileId, setProfileId] = useState('');
  const [msg, setMsg] = useState('');
  
  const users = [
    { id: 1, username: 'admin', password: 'admin123', role: 'admin', email: 'admin@company.com', apiKey: 'sk_live_ABC123' },
    { id: 2, username: 'john', password: 'john123', role: 'user', email: 'john@company.com', apiKey: 'sk_live_USER001' }
  ];
  
  const [posts, setPosts] = useState([
    { id: 1, content: 'Welcome!' }
  ]);
  
  const [files, setFiles] = useState([]);

  function login() {
    const found = users.find(u => u.username === username && u.password === password);
    if (found) {
      setUser({ ...found, token: createToken(found) });
      setTab('dashboard');
      console.log('Login:', found.apiKey); // Bug: logs sensitive data
    } else {
      alert('Invalid login');
    }
  }

  function viewProfile() {
    const target = users.find(u => u.id === parseInt(profileId));
    if (target) {
      alert(`User: ${target.username}\nEmail: ${target.email}\nAPI Key: ${target.apiKey}`);
    }
  }

  function postMsg() {
    if (msg.trim()) {
      setPosts([...posts, { id: posts.length + 1, content: msg }]);
      setMsg('');
    }
  }

  function uploadFile(e) {
    const file = e.target.files[0];
    if (file) {
      setFiles([...files, { name: file.name, size: file.size }]);
      alert(`Uploaded: ${file.name}`);
    }
  }

  if (!user) {
    return (
      <div className="min-h-screen bg-red-50 p-8">
        <div className="max-w-md mx-auto bg-white rounded-lg shadow-xl p-8">
          <div className="flex items-center justify-center mb-6">
            <AlertCircle className="w-10 h-10 text-red-500 mr-2" />
            <h1 className="text-2xl font-bold">Vulnerable App</h1>
          </div>
          
          <div className="bg-red-50 border-l-4 border-red-500 p-3 mb-4 text-sm">
            <p className="text-red-700 font-semibold">⚠️ This app has security bugs</p>
          </div>

          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="w-full px-4 py-2 border rounded mb-3"
            placeholder="Username (admin or john)"
          />
          
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full px-4 py-2 border rounded mb-3"
            placeholder="Password"
          />

          <button onClick={login} className="w-full bg-red-500 text-white py-2 rounded hover:bg-red-600">
            Login
          </button>

          <div className="mt-4 p-3 bg-gray-50 rounded text-xs">
            <p>Test: admin/admin123 or john/john123</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-red-50 p-8">
      <div className="max-w-4xl mx-auto bg-white rounded-lg shadow-xl">
        <div className="bg-red-500 text-white p-4 flex justify-between items-center">
          <div>
            <h1 className="text-xl font-bold">Vulnerable App</h1>
            <p className="text-sm">User: {user.username}</p>
          </div>
          <button onClick={() => setUser(null)} className="bg-red-600 px-4 py-2 rounded">Logout</button>
        </div>

        <div className="flex border-b">
          {['dashboard', 'profiles', 'messages', 'upload'].map(t => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`px-4 py-2 ${tab === t ? 'bg-red-50 border-b-2 border-red-500' : ''}`}
            >
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>

        <div className="p-6">
          {tab === 'dashboard' && (
            <div>
              <h2 className="text-xl font-bold mb-4">Dashboard</h2>
              <div className="bg-yellow-50 border-l-4 border-yellow-400 p-3 text-sm">
                <p className="font-semibold">🔍 Find the bugs in this app!</p>
              </div>
            </div>
          )}

          {tab === 'profiles' && (
            <div>
              <h2 className="text-xl font-bold mb-4">View Profiles (IDOR Bug)</h2>
              <div className="bg-red-50 p-3 mb-4 text-sm">
                <p className="text-red-700">🚨 You can view ANY user's data</p>
              </div>
              <input
                type="text"
                value={profileId}
                onChange={(e) => setProfileId(e.target.value)}
                className="border px-4 py-2 rounded mr-2"
                placeholder="User ID (1 or 2)"
              />
              <button onClick={viewProfile} className="bg-red-500 text-white px-4 py-2 rounded">
                View
              </button>
            </div>
          )}

          {tab === 'messages' && (
            <div>
              <h2 className="text-xl font-bold mb-4">Messages (XSS Bug)</h2>
              <div className="bg-red-50 p-3 mb-4 text-sm">
                <p className="text-red-700">🚨 Try: &lt;img src=x onerror=alert('XSS')&gt;</p>
              </div>
              <textarea
                value={msg}
                onChange={(e) => setMsg(e.target.value)}
                className="w-full border px-4 py-2 rounded mb-2"
                rows="3"
              />
              <button onClick={postMsg} className="bg-red-500 text-white px-4 py-2 rounded">Post</button>
              
              <div className="mt-4 space-y-2">
                {posts.map(p => (
                  <div key={p.id} className="bg-gray-50 p-3 rounded">
                    <div dangerouslySetInnerHTML={{ __html: p.content }} />
                  </div>
                ))}
              </div>
            </div>
          )}

          {tab === 'upload' && (
            <div>
              <h2 className="text-xl font-bold mb-4">Upload (No Validation)</h2>
              <div className="bg-red-50 p-3 mb-4 text-sm">
                <p className="text-red-700">🚨 Upload any file type!</p>
              </div>
              <input type="file" onChange={uploadFile} className="mb-4" />
              
              {files.map((f, i) => (
                <div key={i} className="bg-gray-50 p-2 rounded mb-2">
                  <p className="text-sm">{f.name} ({f.size} bytes)</p>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="p-6 bg-gray-50 border-t">
          <h3 className="font-bold mb-2">Known Bugs:</h3>
          <div className="grid grid-cols-2 gap-2 text-xs">
            <div className="bg-red-100 p-2 rounded">IDOR</div>
            <div className="bg-red-100 p-2 rounded">No Access Control</div>
            <div className="bg-red-100 p-2 rounded">XSS</div>
            <div className="bg-red-100 p-2 rounded">No Upload Validation</div>
            <div className="bg-orange-100 p-2 rounded">Weak JWT (123456)</div>
            <div className="bg-orange-100 p-2 rounded">Data in Console</div>
          </div>
        </div>
      </div>
    </div>
  );
}
