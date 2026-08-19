import React, { useState } from 'react';
import { Modal } from '@/components/ui/Modal';
import { useEmployees } from '@/hooks/useEmployees';

interface EscalationModalProps {
  isOpen: boolean;
  onClose: () => void;
  customerId: number;
  customerName: string;
  aiSummary: string;
  onSubmit: (data: {
    department: string;
    priority: string;
    assigneeId: number | null;
    reason: string;
  }) => Promise<void>;
}

export const EscalationModal: React.FC<EscalationModalProps> = ({
  isOpen,
  onClose,
  customerName,
  aiSummary,
  onSubmit,
}) => {
  const { employees } = useEmployees({ limit: 100 });
  const [department, setDepartment] = useState('Technical Support');
  const [priority, setPriority] = useState('high');
  const [assigneeId, setAssigneeId] = useState<string>('');
  const [reason, setReason] = useState('Low confidence');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    try {
      await onSubmit({
        department,
        priority,
        assigneeId: assigneeId ? parseInt(assigneeId, 10) : null,
        reason,
      });
      onClose();
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Create Escalation" id="escalation-modal">
      <form onSubmit={handleSubmit} className="escalation-form">
        <div className="form-group">
          <label htmlFor="customer-name">Customer</label>
          <input
            id="customer-name"
            type="text"
            className="input-field"
            value={customerName}
            readOnly
            disabled
          />
        </div>

        <div className="form-group">
          <label htmlFor="department">Department</label>
          <select
            id="department"
            className="input-field"
            value={department}
            onChange={(e) => setDepartment(e.target.value)}
          >
            <option value="Technical Support">Technical Support</option>
            <option value="Billing">Billing</option>
            <option value="Customer Success">Customer Success</option>
            <option value="General">General</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="priority">Priority</label>
          <select
            id="priority"
            className="input-field"
            value={priority}
            onChange={(e) => setPriority(e.target.value)}
          >
            <option value="medium">Medium</option>
            <option value="high">High</option>
            <option value="urgent">Urgent</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="assignee">Assign To</label>
          <select
            id="assignee"
            className="input-field"
            value={assigneeId}
            onChange={(e) => setAssigneeId(e.target.value)}
          >
            <option value="">Auto-select</option>
            {employees.map((emp) => (
              <option key={emp.id} value={emp.id}>
                {emp.first_name} {emp.last_name}
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="reason">Escalation Reason</label>
          <select
            id="reason"
            className="input-field"
            value={reason}
            onChange={(e) => setReason(e.target.value)}
          >
            <option value="Low confidence">Low confidence</option>
            <option value="Customer requested human">Customer requested human</option>
            <option value="AI failed repeatedly">AI failed repeatedly</option>
            <option value="Sensitive issue">Sensitive issue</option>
            <option value="Billing dispute">Billing dispute</option>
            <option value="Technical escalation">Technical escalation</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="ai-summary">AI Summary</label>
          <textarea
            id="ai-summary"
            className="input-field"
            style={{ opacity: 0.8 }}
            rows={4}
            value={aiSummary}
            readOnly
          />
        </div>

        <div className="modal-footer" style={{ display: 'flex', gap: '1rem', justifyContent: 'flex-end', marginTop: '1.5rem' }}>
          <button type="button" className="btn btn--secondary" onClick={onClose} disabled={isSubmitting}>
            Cancel
          </button>
          <button type="submit" className="btn btn--primary" disabled={isSubmitting}>
            {isSubmitting ? 'Creating...' : 'Create Escalation'}
          </button>
        </div>
      </form>
    </Modal>
  );
};
