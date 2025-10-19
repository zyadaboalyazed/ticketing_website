import React from 'react';
import { ticketService } from '../../services/ticket.service';
import { contractService } from '../../services/contract.service';
import './Reports.css';

const Reports: React.FC = () => {
  const handleDownload = async (type: 'tickets' | 'contracts', format: 'pdf' | 'csv') => {
    try {
      let blob: Blob;
      let filename: string;

      if (type === 'tickets') {
        if (format === 'pdf') {
          blob = await ticketService.downloadTicketsPDF();
          filename = 'tickets_report.pdf';
        } else {
          blob = await ticketService.downloadTicketsCSV();
          filename = 'tickets_report.csv';
        }
      } else {
        if (format === 'pdf') {
          blob = await contractService.downloadContractsPDF();
          filename = 'contracts_report.pdf';
        } else {
          blob = await contractService.downloadContractsCSV();
          filename = 'contracts_report.csv';
        }
      }

      // Create download link
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Failed to download report:', err);
      alert('Failed to download report');
    }
  };

  return (
    <div className="reports">
      <h1>Reports</h1>

      <div className="report-section">
        <h2>Ticket Reports</h2>
        <p>Download comprehensive reports of all tickets with detailed information.</p>
        <div className="report-buttons">
          <button onClick={() => handleDownload('tickets', 'pdf')} className="btn-primary">
            Download PDF
          </button>
          <button onClick={() => handleDownload('tickets', 'csv')} className="btn-secondary">
            Download CSV
          </button>
        </div>
      </div>

      <div className="report-section">
        <h2>Contract Reports</h2>
        <p>Download reports of all contracts and their details.</p>
        <div className="report-buttons">
          <button onClick={() => handleDownload('contracts', 'pdf')} className="btn-primary">
            Download PDF
          </button>
          <button onClick={() => handleDownload('contracts', 'csv')} className="btn-secondary">
            Download CSV
          </button>
        </div>
      </div>
    </div>
  );
};

export default Reports;
