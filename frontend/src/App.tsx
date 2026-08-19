import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from '@/context/AuthContext';
import Layout from '@/components/layout/Layout';
import LoginPage from '@/pages/LoginPage';
import DashboardPage from '@/pages/DashboardPage';
import ChatPage from '@/pages/ChatPage';
import TicketsPage from '@/pages/TicketsPage';
import TicketDetailPage from '@/pages/TicketDetailPage';
import CustomersPage from '@/pages/CustomersPage';
import CustomerDetailPage from '@/pages/CustomerDetailPage';
import AnalyticsPage from '@/pages/AnalyticsPage';
import BillingPage from '@/pages/BillingPage';
import SettingsPage from '@/pages/SettingsPage';

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          {/* Public */}
          <Route path="/login" element={<LoginPage />} />

          {/* Protected — wrapped in Layout (auth guard inside) */}
          <Route element={<Layout />}>
            <Route index element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<DashboardPage />} />

            {/* Chat */}
            <Route path="/chat" element={<ChatPage />} />
            <Route path="/chat/:conversationId" element={<ChatPage />} />

            {/* Tickets — view as query param: ?view=all|mine|escalated */}
            <Route path="/tickets" element={<TicketsPage />} />
            <Route path="/tickets/:id" element={<TicketDetailPage />} />

            {/* Customers */}
            <Route path="/customers" element={<CustomersPage />} />
            <Route path="/customers/:id" element={<CustomerDetailPage />} />

            {/* Analytics */}
            <Route path="/analytics" element={<AnalyticsPage />} />

            {/* Billing — tab as query param: ?tab=overview|invoices|payments|refunds */}
            <Route path="/billing" element={<BillingPage />} />
            <Route path="/billing/invoices" element={<BillingPage />} />
            <Route path="/billing/payments" element={<BillingPage />} />
            <Route path="/billing/refunds" element={<BillingPage />} />

            {/* Settings — section as query param: ?section=profile|ai|notifications|team */}
            <Route path="/settings" element={<SettingsPage />} />
            <Route path="/settings/profile" element={<SettingsPage />} />
            <Route path="/settings/ai" element={<SettingsPage />} />
            <Route path="/settings/notifications" element={<SettingsPage />} />
            <Route path="/settings/team" element={<SettingsPage />} />
          </Route>

          {/* Fallback */}
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
