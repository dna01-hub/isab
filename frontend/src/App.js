import React, { useState, useEffect } from "react";
import "./App.css";
import { BrowserRouter, Routes, Route, useNavigate, useLocation } from "react-router-dom";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Context for user authentication
const AuthContext = React.createContext();

const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    // Check if user is stored in localStorage
    const storedUser = localStorage.getItem('babyShowerUser');
    if (storedUser) {
      setUser(JSON.parse(storedUser));
      setIsAuthenticated(true);
    }
  }, []);

  const login = (userData) => {
    setUser(userData);
    setIsAuthenticated(true);
    if (userData.stay_connected) {
      localStorage.setItem('babyShowerUser', JSON.stringify(userData));
    }
  };

  const logout = () => {
    setUser(null);
    setIsAuthenticated(false);
    localStorage.removeItem('babyShowerUser');
  };

  return (
    <AuthContext.Provider value={{ user, isAuthenticated, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

// Registration Component
const RegistrationPage = ({ onRegister, onSwitchToLogin }) => {
  const [formData, setFormData] = useState({
    name: '',
    whatsapp: '',
    companions: [],
    stay_connected: false,
    hasCompanions: false
  });
  const [companionName, setCompanionName] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(`${API}/register`, {
        name: formData.name,
        whatsapp: formData.whatsapp,
        companions: formData.companions,
        stay_connected: formData.stay_connected
      });

      onRegister(response.data);
    } catch (error) {
      alert(error.response?.data?.detail || 'Erro no cadastro');
    }
  };

  const addCompanion = () => {
    if (companionName.trim()) {
      setFormData({
        ...formData,
        companions: [...formData.companions, companionName.trim()]
      });
      setCompanionName('');
    }
  };

  const removeCompanion = (index) => {
    setFormData({
      ...formData,
      companions: formData.companions.filter((_, i) => i !== index)
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-100 via-rose-50 to-purple-100 flex items-center justify-center p-4">
      <div className="max-w-md w-full">
        {/* Header */}
        <div className="text-center mb-8 animate-fade-in">
          <div className="relative mb-6">
            <img 
              src="https://images.unsplash.com/photo-1622290291165-d341f1938b8a?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDJ8MHwxfHNlYXJjaHwzfHxiYWJ5JTIwc2hvd2VyfGVufDB8fHx8MTc1MzQ5OTYwMXww&ixlib=rb-4.1.0&q=85"
              alt="Baby Shower"
              className="w-32 h-32 rounded-full mx-auto shadow-2xl border-4 border-white object-cover"
            />
            <div className="absolute -top-2 -right-2">
              <span className="inline-flex items-center justify-center w-8 h-8 bg-pink-500 text-white rounded-full text-lg animate-bounce">
                👶
              </span>
            </div>
          </div>
          <h1 className="text-4xl font-bold bg-gradient-to-r from-pink-600 to-purple-600 bg-clip-text text-transparent">
            Chá de Bebê
          </h1>
          <h2 className="text-2xl font-semibold text-rose-800 mt-2">
            Isadora & Isabelle
          </h2>
          <p className="text-gray-600 mt-2">09/08/2025 • Local: A definir</p>
        </div>

        {/* Registration Form */}
        <div className="bg-white rounded-3xl shadow-2xl p-8 backdrop-blur-sm bg-opacity-95">
          <h3 className="text-2xl font-bold text-center text-gray-800 mb-6">
            Confirme sua Presença
          </h3>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Nome Completo
              </label>
              <input
                type="text"
                value={formData.name}
                onChange={(e) => setFormData({...formData, name: e.target.value})}
                required
                className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-pink-500 focus:border-transparent transition-all duration-300"
                placeholder="Digite seu nome completo"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                WhatsApp
              </label>
              <input
                type="tel"
                value={formData.whatsapp}
                onChange={(e) => setFormData({...formData, whatsapp: e.target.value})}
                required
                className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-pink-500 focus:border-transparent transition-all duration-300"
                placeholder="(xx) xxxxx-xxxx"
              />
            </div>

            <div>
              <label className="flex items-center space-x-3">
                <input
                  type="checkbox"
                  checked={formData.hasCompanions}
                  onChange={(e) => setFormData({...formData, hasCompanions: e.target.checked})}
                  className="w-5 h-5 text-pink-600 rounded focus:ring-pink-500"
                />
                <span className="text-sm font-medium text-gray-700">
                  Vou levar acompanhantes
                </span>
              </label>
            </div>

            {formData.hasCompanions && (
              <div className="space-y-3">
                <div className="flex space-x-2">
                  <input
                    type="text"
                    value={companionName}
                    onChange={(e) => setCompanionName(e.target.value)}
                    className="flex-1 px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-pink-500"
                    placeholder="Nome do acompanhante"
                  />
                  <button
                    type="button"
                    onClick={addCompanion}
                    className="px-4 py-3 bg-pink-500 text-white rounded-xl hover:bg-pink-600 transition-colors"
                  >
                    Adicionar
                  </button>
                </div>
                
                {formData.companions.length > 0 && (
                  <div className="space-y-2">
                    <p className="text-sm font-medium text-gray-700">Acompanhantes:</p>
                    {formData.companions.map((companion, index) => (
                      <div key={index} className="flex items-center justify-between bg-pink-50 px-3 py-2 rounded-lg">
                        <span>{companion}</span>
                        <button
                          type="button"
                          onClick={() => removeCompanion(index)}
                          className="text-red-500 hover:text-red-700"
                        >
                          ✕
                        </button>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}

            <div>
              <label className="flex items-center space-x-3">
                <input
                  type="checkbox"
                  checked={formData.stay_connected}
                  onChange={(e) => setFormData({...formData, stay_connected: e.target.checked})}
                  className="w-5 h-5 text-pink-600 rounded focus:ring-pink-500"
                />
                <span className="text-sm font-medium text-gray-700">
                  Manter conectado
                </span>
              </label>
            </div>

            <button
              type="submit"
              className="w-full bg-gradient-to-r from-pink-500 to-purple-500 text-white py-4 rounded-xl font-semibold text-lg hover:from-pink-600 hover:to-purple-600 transform hover:scale-105 transition-all duration-300 shadow-lg"
            >
              Confirmar Presença
            </button>
          </form>

          <div className="mt-4 text-center">
            <button
              onClick={onSwitchToLogin}
              className="text-pink-600 hover:text-pink-800 font-medium text-sm"
            >
              Já sou cadastrado - Fazer Login
            </button>
          </div>
        </div>

        {/* Footer */}
        <div className="text-center mt-8 text-gray-600">
          <p className="text-sm">
            Contato: Daniel • (69) 99226-5294
          </p>
          <div className="mt-4">
            <a 
              href="/admin"
              className="inline-flex items-center space-x-1 text-xs text-gray-400 hover:text-gray-600 transition-colors"
            >
              <span>🔐</span>
              <span>Painel Admin</span>
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

// Login Component
const LoginPage = ({ onLogin, onSwitchToRegister }) => {
  const [loginData, setLoginData] = useState({
    name: '',
    whatsapp: ''
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(`${API}/login`, loginData);
      onLogin(response.data);
    } catch (error) {
      alert(error.response?.data?.detail || 'Erro no login');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-100 via-rose-50 to-purple-100 flex items-center justify-center p-4">
      <div className="max-w-md w-full">
        <div className="text-center mb-8 animate-fade-in">
          <div className="relative mb-6">
            <img 
              src="https://images.unsplash.com/photo-1597413545419-4013431dbfec?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzh8MHwxfHNlYXJjaHwxfHx0d2luc3xlbnwwfHx8fDE3NTM0OTk2MDl8MA&ixlib=rb-4.1.0&q=85"
              alt="Twins"
              className="w-32 h-32 rounded-full mx-auto shadow-2xl border-4 border-white object-cover"
            />
          </div>
          <h1 className="text-4xl font-bold bg-gradient-to-r from-pink-600 to-purple-600 bg-clip-text text-transparent">
            Bem-vindo de volta!
          </h1>
          <h2 className="text-2xl font-semibold text-rose-800 mt-2">
            Faça seu login
          </h2>
        </div>

        <div className="bg-white rounded-3xl shadow-2xl p-8 backdrop-blur-sm bg-opacity-95">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Nome Completo
              </label>
              <input
                type="text"
                value={loginData.name}
                onChange={(e) => setLoginData({...loginData, name: e.target.value})}
                required
                className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-pink-500 focus:border-transparent transition-all duration-300"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                WhatsApp
              </label>
              <input
                type="tel"
                value={loginData.whatsapp}
                onChange={(e) => setLoginData({...loginData, whatsapp: e.target.value})}
                required
                className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-pink-500 focus:border-transparent transition-all duration-300"
              />
            </div>

            <button
              type="submit"
              className="w-full bg-gradient-to-r from-pink-500 to-purple-500 text-white py-4 rounded-xl font-semibold text-lg hover:from-pink-600 hover:to-purple-600 transform hover:scale-105 transition-all duration-300 shadow-lg"
            >
              Entrar
            </button>
          </form>

          <div className="mt-4 text-center">
            <button
              onClick={onSwitchToRegister}
              className="text-pink-600 hover:text-pink-800 font-medium text-sm"
            >
              Não sou cadastrado - Fazer Cadastro
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

// Main Event Page
const EventPage = ({ user, onLogout }) => {
  const [currentView, setCurrentView] = useState('home');
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [gifts, setGifts] = useState([]);
  const [userReservations, setUserReservations] = useState([]);
  const [showAdminLogin, setShowAdminLogin] = useState(false);
  const [adminCredentials, setAdminCredentials] = useState({ username: '', password: '' });
  const [adminData, setAdminData] = useState(null);

  const categories = [
    { id: 'fraldas', name: 'Fraldas', icon: '👶', color: 'from-pink-400 to-pink-600' },
    { id: 'roupas', name: 'Roupas', icon: '👕', color: 'from-purple-400 to-purple-600' },
    { id: 'higiene', name: 'Higiene', icon: '🧴', color: 'from-blue-400 to-blue-600' },
    { id: 'alimentacao', name: 'Alimentação', icon: '🍼', color: 'from-green-400 to-green-600' },
    { id: 'quarto', name: 'Quarto', icon: '🛏️', color: 'from-yellow-400 to-yellow-600' },
    { id: 'passeio', name: 'Passeio', icon: '🚁', color: 'from-indigo-400 to-indigo-600' }
  ];

  useEffect(() => {
    fetchUserReservations();
  }, [user]);

  const fetchUserReservations = async () => {
    try {
      const response = await axios.get(`${API}/user/${user.id}/reservations`);
      setUserReservations(response.data);
    } catch (error) {
      console.error('Error fetching reservations:', error);
    }
  };

  const fetchGifts = async (category) => {
    try {
      const response = await axios.get(`${API}/gifts/${category}`);
      setGifts(response.data);
    } catch (error) {
      console.error('Error fetching gifts:', error);
    }
  };

  const handleCategorySelect = (category) => {
    setSelectedCategory(category);
    setCurrentView('gifts');
    fetchGifts(category.id);
  };

  const handleGiftReserve = async (gift, quantity = 1) => {
    try {
      await axios.post(`${API}/reserve-gift`, {
        user_id: user.id,
        gift_id: gift.id,
        quantity: quantity
      });
      
      // Show success animation
      showSuccessAnimation();
      
      // Refresh gifts and reservations
      fetchGifts(selectedCategory.id);
      fetchUserReservations();
      
    } catch (error) {
      alert(error.response?.data?.detail || 'Erro ao reservar presente');
    }
  };

  const showSuccessAnimation = () => {
    const heart = document.createElement('div');
    heart.innerHTML = '💖';
    heart.className = 'fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-6xl animate-bounce z-50';
    document.body.appendChild(heart);
    
    setTimeout(() => {
      heart.remove();
    }, 2000);
  };

  const handleAdminLogin = async () => {
    try {
      await axios.post(`${API}/admin/login`, adminCredentials);
      const dashboardResponse = await axios.get(`${API}/admin/dashboard`);
      setAdminData(dashboardResponse.data);
      setCurrentView('admin');
      setShowAdminLogin(false);
    } catch (error) {
      alert('Credenciais inválidas');
    }
  };

  // Admin keyboard shortcut
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.ctrlKey && e.shiftKey && e.key === 'A') {
        e.preventDefault();
        setShowAdminLogin(true);
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, []);

  if (currentView === 'admin' && adminData) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 p-4">
        <div className="max-w-6xl mx-auto">
          <div className="bg-white rounded-3xl shadow-2xl p-8">
            <div className="flex justify-between items-center mb-8">
              <h1 className="text-3xl font-bold text-gray-800">Dashboard Administrativo</h1>
              <button
                onClick={() => setCurrentView('home')}
                className="px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600"
              >
                Voltar
              </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
              <div className="bg-pink-100 p-6 rounded-xl text-center">
                <h3 className="text-2xl font-bold text-pink-600">{adminData.total_confirmed}</h3>
                <p className="text-pink-800">Confirmados</p>
              </div>
              <div className="bg-purple-100 p-6 rounded-xl text-center">
                <h3 className="text-2xl font-bold text-purple-600">{adminData.total_companions}</h3>
                <p className="text-purple-800">Acompanhantes</p>
              </div>
              <div className="bg-blue-100 p-6 rounded-xl text-center">
                <h3 className="text-2xl font-bold text-blue-600">{adminData.total_attendees}</h3>
                <p className="text-blue-800">Total Pessoas</p>
              </div>
              <div className="bg-green-100 p-6 rounded-xl text-center">
                <h3 className="text-2xl font-bold text-green-600">{adminData.total_gifts_reserved}</h3>
                <p className="text-green-800">Presentes Reservados</p>
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <div>
                <h2 className="text-xl font-bold mb-4">Convidados Confirmados</h2>
                <div className="bg-gray-50 rounded-xl p-4 max-h-80 overflow-y-auto">
                  {adminData.users.map((user, index) => (
                    <div key={index} className="mb-3 p-3 bg-white rounded-lg">
                      <p className="font-semibold">{user.name}</p>
                      <p className="text-sm text-gray-600">{user.whatsapp}</p>
                      {user.companions.length > 0 && (
                        <p className="text-sm text-gray-500">
                          Acompanhantes: {user.companions.join(', ')}
                        </p>
                      )}
                    </div>
                  ))}
                </div>
              </div>

              <div>
                <h2 className="text-xl font-bold mb-4">Presentes Reservados</h2>
                <div className="bg-gray-50 rounded-xl p-4 max-h-80 overflow-y-auto">
                  {adminData.reservations.map((reservation, index) => (
                    <div key={index} className="mb-3 p-3 bg-white rounded-lg">
                      <p className="font-semibold">{reservation.user_name}</p>
                      <p className="text-sm text-gray-600">{reservation.gift_name}</p>
                      <p className="text-sm text-gray-500">Qtd: {reservation.quantity}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (currentView === 'gifts' && selectedCategory) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-pink-50 to-purple-50 p-4">
        <div className="max-w-4xl mx-auto">
          <div className="flex items-center justify-between mb-8">
            <button
              onClick={() => setCurrentView('home')}
              className="flex items-center space-x-2 px-4 py-2 bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow"
            >
              <span>←</span>
              <span>Voltar</span>
            </button>
            <h1 className="text-2xl font-bold text-gray-800">
              {selectedCategory.icon} {selectedCategory.name}
            </h1>
            <div></div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {gifts.map((gift) => (
              <div key={gift.id} className="bg-white rounded-2xl shadow-lg overflow-hidden hover:shadow-xl transition-shadow">
                <img 
                  src={gift.image_url} 
                  alt={gift.name}
                  className="w-full h-48 object-cover"
                />
                <div className="p-6">
                  <h3 className="font-bold text-lg mb-2">{gift.name}</h3>
                  <p className="text-gray-600 text-sm mb-3">{gift.description}</p>
                  <p className="text-pink-600 font-semibold mb-2">{gift.price_range}</p>
                  <p className="text-sm text-gray-500 mb-4">
                    Disponível: {gift.available_quantity} de {gift.quantity}
                  </p>
                  
                  {gift.buy_link && (
                    <a 
                      href={gift.buy_link}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-block mb-3 text-blue-600 hover:text-blue-800 text-sm"
                    >
                      Ver onde comprar →
                    </a>
                  )}
                  
                  <button
                    onClick={() => handleGiftReserve(gift)}
                    disabled={!gift.is_available}
                    className={`w-full py-3 rounded-xl font-semibold transition-all duration-300 ${
                      gift.is_available 
                        ? 'bg-gradient-to-r from-pink-500 to-purple-500 text-white hover:from-pink-600 hover:to-purple-600 transform hover:scale-105' 
                        : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                    }`}
                  >
                    {gift.is_available ? 'Escolher Este Presente' : 'Indisponível'}
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-100 via-rose-50 to-purple-100">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        <div className="absolute inset-0">
          <img 
            src="https://images.unsplash.com/photo-1622290319146-7b63df48a635?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDJ8MHwxfHNlYXJjaHwyfHxiYWJ5JTIwc2hvd2VyfGVufDB8fHx8MTc1MzQ5OTYwMXww&ixlib=rb-4.1.0&q=85"
            alt="Baby Shower Background"
            className="w-full h-full object-cover opacity-20"
          />
          <div className="absolute inset-0 bg-gradient-to-br from-pink-400/30 to-purple-400/30"></div>
        </div>
        
        <div className="relative z-10 p-8 text-center">
          <div className="max-w-4xl mx-auto">
            <div className="flex justify-between items-center mb-8">
              <div className="text-left">
                <p className="text-pink-800 font-medium">
                  Olá, {user.name}! 👋
                </p>
              </div>
              <button
                onClick={onLogout}
                className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors"
              >
                Sair
              </button>
            </div>

            <div className="mb-8 animate-fade-in">
              <h1 className="text-5xl font-bold bg-gradient-to-r from-pink-600 to-purple-600 bg-clip-text text-transparent mb-4">
                Chá de Bebê
              </h1>
              <h2 className="text-3xl font-semibold text-rose-800 mb-6">
                Isadora & Isabelle
              </h2>
              
              <div className="bg-white/80 backdrop-blur-sm rounded-2xl p-6 mx-auto max-w-md shadow-xl">
                <div className="text-gray-800">
                  <div className="flex items-center justify-center space-x-4 mb-4">
                    <div className="text-center">
                      <p className="font-bold text-lg">📅 Data</p>
                      <p>09 de Agosto, 2025</p>
                    </div>
                    <div className="h-12 w-px bg-gray-300"></div>
                    <div className="text-center">
                      <p className="font-bold text-lg">📍 Local</p>
                      <p>A definir</p>
                    </div>
                  </div>
                  <div className="text-center border-t pt-4">
                    <p className="font-bold text-lg">📞 Contato</p>
                    <p>Daniel: (69) 99226-5294</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Categories Section */}
      <div className="p-8">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center text-gray-800 mb-12">
            Lista de Presentes
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {categories.map((category) => (
              <div
                key={category.id}
                onClick={() => handleCategorySelect(category)}
                className="group cursor-pointer"
              >
                <div className={`bg-gradient-to-br ${category.color} p-8 rounded-3xl shadow-xl hover:shadow-2xl transform hover:scale-105 transition-all duration-500 text-white text-center`}>
                  <div className="text-6xl mb-4 group-hover:animate-bounce">
                    {category.icon}
                  </div>
                  <h3 className="text-2xl font-bold mb-2">
                    {category.name}
                  </h3>
                  <p className="text-white/80">
                    Clique para ver os presentes
                  </p>
                </div>
              </div>
            ))}
          </div>

          {/* User Reservations */}
          {userReservations.length > 0 && (
            <div className="mt-16">
              <h2 className="text-2xl font-bold text-center text-gray-800 mb-8">
                Seus Presentes Escolhidos 💝
              </h2>
              <div className="bg-white rounded-3xl shadow-xl p-8">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {userReservations.map((item, index) => (
                    <div key={index} className="bg-pink-50 p-4 rounded-xl">
                      <img 
                        src={item.gift.image_url} 
                        alt={item.gift.name}
                        className="w-full h-32 object-cover rounded-lg mb-3"
                      />
                      <h4 className="font-bold text-gray-800">{item.gift.name}</h4>
                      <p className="text-sm text-gray-600">Qtd: {item.reservation.quantity}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Admin Login Modal */}
      {showAdminLogin && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl p-6 max-w-md w-full">
            <h3 className="text-xl font-bold mb-4">Login Administrativo</h3>
            <div className="space-y-4">
              <input
                type="text"
                placeholder="Usuário"
                value={adminCredentials.username}
                onChange={(e) => setAdminCredentials({...adminCredentials, username: e.target.value})}
                className="w-full px-3 py-2 border rounded-lg"
              />
              <input
                type="password"
                placeholder="Senha"
                value={adminCredentials.password}
                onChange={(e) => setAdminCredentials({...adminCredentials, password: e.target.value})}
                className="w-full px-3 py-2 border rounded-lg"
              />
              <div className="flex space-x-3">
                <button
                  onClick={handleAdminLogin}
                  className="flex-1 bg-blue-500 text-white py-2 rounded-lg hover:bg-blue-600"
                >
                  Entrar
                </button>
                <button
                  onClick={() => setShowAdminLogin(false)}
                  className="flex-1 bg-gray-500 text-white py-2 rounded-lg hover:bg-gray-600"
                >
                  Cancelar
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

// Admin Login Page Component
const AdminLoginPage = () => {
  const [credentials, setCredentials] = useState({ username: '', password: '' });
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleAdminLogin = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    
    try {
      await axios.post(`${API}/admin/login`, credentials);
      const dashboardResponse = await axios.get(`${API}/admin/dashboard`);
      
      // Store admin session
      localStorage.setItem('adminSession', JSON.stringify({
        loggedIn: true,
        data: dashboardResponse.data,
        timestamp: new Date().getTime()
      }));
      
      navigate('/admin/dashboard');
    } catch (error) {
      alert('Credenciais inválidas. Verifique usuário e senha.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-100 via-slate-50 to-gray-200 flex items-center justify-center p-4">
      <div className="max-w-md w-full">
        <div className="text-center mb-8">
          <div className="relative mb-6">
            <div className="w-24 h-24 bg-gradient-to-r from-gray-600 to-gray-800 rounded-full mx-auto flex items-center justify-center shadow-2xl">
              <span className="text-4xl text-white">🔐</span>
            </div>
          </div>
          <h1 className="text-3xl font-bold text-gray-800 mb-2">
            Painel Administrativo
          </h1>
          <p className="text-gray-600">Chá de Bebê - Isadora & Isabelle</p>
        </div>

        <div className="bg-white rounded-3xl shadow-2xl p-8">
          <form onSubmit={handleAdminLogin} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Usuário
              </label>
              <input
                type="text"
                value={credentials.username}
                onChange={(e) => setCredentials({...credentials, username: e.target.value})}
                required
                className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-gray-500 focus:border-transparent transition-all duration-300"
                placeholder="Digite o usuário"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Senha
              </label>
              <input
                type="password"
                value={credentials.password}
                onChange={(e) => setCredentials({...credentials, password: e.target.value})}
                required
                className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-gray-500 focus:border-transparent transition-all duration-300"
                placeholder="Digite a senha"
              />
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-gradient-to-r from-gray-600 to-gray-800 text-white py-4 rounded-xl font-semibold text-lg hover:from-gray-700 hover:to-gray-900 transform hover:scale-105 transition-all duration-300 shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? 'Entrando...' : 'Acessar Painel'}
            </button>
          </form>

          <div className="mt-6 text-center">
            <button
              onClick={() => navigate('/')}
              className="text-gray-600 hover:text-gray-800 font-medium text-sm flex items-center justify-center space-x-2"
            >
              <span>←</span>
              <span>Voltar ao Site</span>
            </button>
          </div>
        </div>

        <div className="text-center mt-6 text-gray-500 text-sm">
          <p>Acesso restrito aos organizadores do evento</p>
        </div>
      </div>
    </div>
  );
};

// Admin Dashboard Component
const AdminDashboard = () => {
  const [adminData, setAdminData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    // Check admin session and load data
    const adminSession = localStorage.getItem('adminSession');
    if (!adminSession) {
      navigate('/admin');
      return;
    }

    try {
      const session = JSON.parse(adminSession);
      if (session.loggedIn && session.data) {
        // Check if session is not too old (2 hours)
        const now = new Date().getTime();
        if (now - session.timestamp < 2 * 60 * 60 * 1000) {
          setAdminData(session.data);
          setIsLoading(false);
        } else {
          // Session expired
          handleLogout();
        }
      } else {
        navigate('/admin');
      }
    } catch (error) {
      navigate('/admin');
    }
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem('adminSession');
    navigate('/admin');
  };

  const refreshData = async () => {
    try {
      setIsLoading(true);
      const response = await axios.get(`${API}/admin/dashboard`);
      setAdminData(response.data);
      
      // Update stored session
      localStorage.setItem('adminSession', JSON.stringify({
        loggedIn: true,
        data: response.data,
        timestamp: new Date().getTime()
      }));
    } catch (error) {
      alert('Erro ao atualizar dados. Faça login novamente.');
      handleLogout();
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading || !adminData) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-gray-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Carregando painel administrativo...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 p-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-3xl shadow-xl p-6 mb-8">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-gray-800 mb-2">
                🎀 Dashboard Administrativo
              </h1>
              <p className="text-gray-600">
                Chá de Bebê - Isadora & Isabelle • Atualizado: {new Date().toLocaleString('pt-BR')}
              </p>
            </div>
            <div className="flex space-x-3">
              <button
                onClick={refreshData}
                disabled={isLoading}
                className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors disabled:opacity-50"
              >
                🔄 Atualizar
              </button>
              <button
                onClick={() => navigate('/')}
                className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors"
              >
                🏠 Site Principal
              </button>
              <button
                onClick={handleLogout}
                className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors"
              >
                🚪 Sair
              </button>
            </div>
          </div>
        </div>

        {/* Statistics Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-gradient-to-r from-pink-400 to-pink-600 p-6 rounded-2xl text-white shadow-lg">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-3xl font-bold">{adminData.total_confirmed}</h3>
                <p className="text-pink-100 font-medium">Confirmados</p>
              </div>
              <span className="text-4xl opacity-80">👥</span>
            </div>
          </div>
          
          <div className="bg-gradient-to-r from-purple-400 to-purple-600 p-6 rounded-2xl text-white shadow-lg">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-3xl font-bold">{adminData.total_companions}</h3>
                <p className="text-purple-100 font-medium">Acompanhantes</p>
              </div>
              <span className="text-4xl opacity-80">👫</span>
            </div>
          </div>
          
          <div className="bg-gradient-to-r from-blue-400 to-blue-600 p-6 rounded-2xl text-white shadow-lg">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-3xl font-bold">{adminData.total_attendees}</h3>
                <p className="text-blue-100 font-medium">Total Pessoas</p>
              </div>
              <span className="text-4xl opacity-80">🎉</span>
            </div>
          </div>
          
          <div className="bg-gradient-to-r from-green-400 to-green-600 p-6 rounded-2xl text-white shadow-lg">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-3xl font-bold">{adminData.total_gifts_reserved}</h3>
                <p className="text-green-100 font-medium">Presentes Reservados</p>
              </div>
              <span className="text-4xl opacity-80">🎁</span>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Confirmed Guests */}
          <div className="bg-white rounded-3xl shadow-xl p-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-6 flex items-center">
              <span className="mr-3">👥</span>
              Convidados Confirmados ({adminData.total_confirmed})
            </h2>
            <div className="max-h-96 overflow-y-auto custom-scrollbar space-y-4">
              {adminData.users.map((user, index) => (
                <div key={index} className="bg-gray-50 rounded-xl p-4 hover:bg-gray-100 transition-colors">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <h3 className="font-bold text-gray-800">{user.name}</h3>
                      <p className="text-sm text-gray-600 flex items-center mt-1">
                        <span className="mr-1">📱</span>
                        {user.whatsapp}
                      </p>
                      {user.companions && user.companions.length > 0 && (
                        <div className="mt-2">
                          <p className="text-sm font-medium text-gray-700">Acompanhantes:</p>
                          <div className="flex flex-wrap gap-1 mt-1">
                            {user.companions.map((companion, i) => (
                              <span key={i} className="inline-block bg-pink-100 text-pink-800 px-2 py-1 rounded-lg text-xs">
                                {companion}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                    <div className="text-right">
                      <span className="inline-block bg-green-100 text-green-800 px-2 py-1 rounded-lg text-xs font-medium">
                        ✅ Confirmado
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Reserved Gifts */}
          <div className="bg-white rounded-3xl shadow-xl p-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-6 flex items-center">
              <span className="mr-3">🎁</span>
              Presentes Reservados ({adminData.total_gifts_reserved})
            </h2>
            <div className="max-h-96 overflow-y-auto custom-scrollbar space-y-4">
              {adminData.reservations.map((reservation, index) => (
                <div key={index} className="bg-gray-50 rounded-xl p-4 hover:bg-gray-100 transition-colors">
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <h3 className="font-bold text-gray-800">{reservation.gift_name}</h3>
                      <p className="text-sm text-gray-600 mt-1">
                        <span className="font-medium">Por:</span> {reservation.user_name}
                      </p>
                      <p className="text-xs text-gray-500 mt-1">
                        Qtd: {reservation.quantity} • {new Date(reservation.reserved_at).toLocaleString('pt-BR')}
                      </p>
                    </div>
                    <span className="inline-block bg-purple-100 text-purple-800 px-2 py-1 rounded-lg text-xs font-medium">
                      📦 Reservado
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Available Gifts */}
        <div className="mt-8 bg-white rounded-3xl shadow-xl p-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-6 flex items-center">
            <span className="mr-3">📋</span>
            Presentes Ainda Disponíveis ({adminData.available_gifts.length})
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {adminData.available_gifts.map((gift, index) => (
              <div key={index} className="bg-blue-50 rounded-xl p-4 border border-blue-200">
                <h3 className="font-bold text-gray-800">{gift.name}</h3>
                <p className="text-sm text-blue-600 mt-1">
                  Disponível: {gift.available_quantity}
                </p>
              </div>
            ))}
          </div>
          {adminData.available_gifts.length === 0 && (
            <div className="text-center py-8">
              <span className="text-6xl mb-4 block">🎉</span>
              <p className="text-xl font-bold text-gray-800">
                Todos os presentes foram reservados!
              </p>
              <p className="text-gray-600 mt-2">
                Parabéns! O chá de bebê foi um sucesso!
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

// Main App Component  
function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/admin" element={<AdminLoginPage />} />
        <Route path="/admin/dashboard" element={<AdminDashboard />} />
        <Route path="/*" element={<MainApp />} />
      </Routes>
    </BrowserRouter>
  );
}

// Main Application Logic
function MainApp() {
  const [currentPage, setCurrentPage] = useState('register');
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    // Check if user is stored in localStorage
    const storedUser = localStorage.getItem('babyShowerUser');
    if (storedUser) {
      const userData = JSON.parse(storedUser);
      setUser(userData);
      setIsAuthenticated(true);
    }
  }, []);

  const handleRegister = (userData) => {
    setUser(userData);
    setIsAuthenticated(true);
    if (userData.stay_connected) {
      localStorage.setItem('babyShowerUser', JSON.stringify(userData));
    }
  };

  const handleLogin = (userData) => {
    setUser(userData);
    setIsAuthenticated(true);
    if (userData.stay_connected) {
      localStorage.setItem('babyShowerUser', JSON.stringify(userData));
    }
  };

  const handleLogout = () => {
    setUser(null);
    setIsAuthenticated(false);
    localStorage.removeItem('babyShowerUser');
  };

  if (isAuthenticated && user) {
    return <EventPage user={user} onLogout={handleLogout} />;
  }

  if (currentPage === 'login') {
    return (
      <LoginPage 
        onLogin={handleLogin}
        onSwitchToRegister={() => setCurrentPage('register')}
      />
    );
  }

  return (
    <RegistrationPage 
      onRegister={handleRegister}
      onSwitchToLogin={() => setCurrentPage('login')}
    />
  );
}

export default App;