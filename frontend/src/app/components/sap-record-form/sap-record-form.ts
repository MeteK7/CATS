import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';
import { SapDataService } from '../../services/sap-data.service';
import { SAPRecord } from '../../models/sap-record.model';

@Component({
  selector: 'app-sap-record-form',
  imports: [CommonModule, FormsModule],
  templateUrl: './sap-record-form.html',
  styleUrl: './sap-record-form.css'
})
export class SapRecordForm implements OnInit {
  record: SAPRecord = { data: {} };
  isEditMode = false;
  loading = false;
  error: string | null = null;
  newFieldKey = '';
  newFieldValue = '';

  constructor(
    private sapDataService: SapDataService,
    private router: Router,
    private route: ActivatedRoute
  ) {}

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (id && id !== 'new') {
      this.isEditMode = true;
      this.loadRecord(id);
    }
  }

  loadRecord(id: string): void {
    this.loading = true;
    this.sapDataService.getRecord(id).subscribe({
      next: (record) => {
        this.record = record;
        this.loading = false;
      },
      error: (error) => {
        this.error = 'Failed to load record: ' + error.message;
        this.loading = false;
      }
    });
  }

  addField(): void {
    if (this.newFieldKey && this.newFieldValue) {
      this.record.data[this.newFieldKey] = this.newFieldValue;
      this.newFieldKey = '';
      this.newFieldValue = '';
    }
  }

  removeField(key: string): void {
    delete this.record.data[key];
  }

  getDataKeys(): string[] {
    return Object.keys(this.record.data);
  }

  onSubmit(): void {
    this.loading = true;
    this.error = null;

    const operation = this.isEditMode 
      ? this.sapDataService.updateRecord(this.record.id!, this.record)
      : this.sapDataService.createRecord(this.record);

    operation.subscribe({
      next: (response) => {
        if (response.success) {
          this.router.navigate(['/records']);
        } else {
          this.error = 'Failed to save record: ' + response.message;
          this.loading = false;
        }
      },
      error: (error) => {
        this.error = 'Failed to save record: ' + error.message;
        this.loading = false;
      }
    });
  }

  cancel(): void {
    this.router.navigate(['/records']);
  }
}
