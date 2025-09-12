import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { SapDataService } from '../../services/sap-data.service';
import { SAPRecord } from '../../models/sap-record.model';

@Component({
  selector: 'app-sap-record-list',
  imports: [CommonModule, RouterModule],
  templateUrl: './sap-record-list.html',
  styleUrl: './sap-record-list.css'
})
export class SapRecordList implements OnInit {
  records: SAPRecord[] = [];
  loading = false;
  error: string | null = null;

  constructor(private sapDataService: SapDataService) {}

  ngOnInit(): void {
    this.loadRecords();
  }

  loadRecords(): void {
    this.loading = true;
    this.error = null;
    
    this.sapDataService.getAllRecords().subscribe({
      next: (records) => {
        this.records = records;
        this.loading = false;
      },
      error: (error) => {
        this.error = 'Failed to load SAP records: ' + error.message;
        this.loading = false;
        console.error('Error loading records:', error);
      }
    });
  }

  deleteRecord(id: string): void {
    if (confirm('Are you sure you want to delete this record?')) {
      this.sapDataService.deleteRecord(id).subscribe({
        next: (response) => {
          if (response.success) {
            this.records = this.records.filter(record => record.id !== id);
          } else {
            this.error = 'Failed to delete record: ' + response.message;
          }
        },
        error: (error) => {
          this.error = 'Failed to delete record: ' + error.message;
          console.error('Error deleting record:', error);
        }
      });
    }
  }

  refreshRecords(): void {
    this.loadRecords();
  }
}
