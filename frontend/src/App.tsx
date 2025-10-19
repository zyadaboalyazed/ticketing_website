import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import Layout from './components/common/Layout';
import ProtectedRoute from './components/common/ProtectedRoute';
import Login from './components/auth/Login';
import Register from './components/auth/Register';
import Dashboard from './components/dashboard/Dashboard';
import TicketList from './components/tickets/TicketList';
import TicketDetail from './components/tickets/TicketDetail';
import CreateTicket from './components/tickets/CreateTicket';
import Reports from './pages/Reports';
import { UserRole } from './types/auth';
import './App.css';

function AppRoutes() {
  const { user } = useAuth();

  return (
    <Routes>
      <Route path="/login" element={user ? <Navigate to="/" /> : <Login />} />
      <Route path="/register" element={user ? <Navigate to="/" /> : <Register />} />
      
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <Layout>
              <Dashboard />
            </Layout>
          </ProtectedRoute>
        }
      />
      
      <Route
        path="/tickets"
        element={
          <ProtectedRoute>
            <Layout>
              <TicketList />
            </Layout>
          </ProtectedRoute>
        }
      />
      
      <Route
        path="/tickets/new"
        element={
          <ProtectedRoute allowedRoles={[UserRole.CLIENT]}>
            <Layout>
              <CreateTicket />
            </Layout>
          </ProtectedRoute>
        }
      />
      
      <Route
        path="/tickets/:id"
        element={
          <ProtectedRoute>
            <Layout>
              <TicketDetail />
            </Layout>
          </ProtectedRoute>
        }
      />
      
      <Route
        path="/reports"
        element={
          <ProtectedRoute allowedRoles={[UserRole.ADMIN, UserRole.AGENT]}>
            <Layout>
              <Reports />
            </Layout>
          </ProtectedRoute>
        }
      />
      
      <Route path="*" element={<Navigate to="/" />} />
    </Routes>
  );
}

function App() {
  return (
    <Router>
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </Router>
  );
}

export default App;
