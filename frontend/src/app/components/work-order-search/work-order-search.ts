import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { WorkOrderService } from '../../services/work-order.service';

interface DropdownOption {
  value: string;
  text: string;
}

interface WorkOrderSearchRequest {
  i_lang: string;
  i_usercode: string;
  vin?: string;
  dealer_code?: string;
  wo_no?: string;
  date_from?: string;
  date_to?: string;
  temsa_global?: boolean;
  temsa_global_gwk?: boolean;
  germany?: boolean;
  france?: boolean;
  north_america?: boolean;
}

interface WorkOrderItem {
  credate?: string;
  dealer_code?: string;
  vin?: string;
  wo_status?: string;
  wo_status_text?: string;
  wo_type?: string;
  wo_type_text?: string;
  fg_status_text?: string;
  pds?: string;
  demo?: string;
  wono?: string;
  creuser?: string;
  ra_country_text?: string;
  wo_onay_text?: string;
  reject_note?: string;
  enability_button?: boolean;
}

interface SearchFormData {
  // No dropdown data needed for simplified search
}

@Component({
  selector: 'app-work-order-search',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './work-order-search.html',
  styleUrls: ['./work-order-search.css']
})
export class WorkOrderSearchComponent implements OnInit {
  // Search form data
  formData: SearchFormData = {};

  // Search criteria
  searchCriteria: WorkOrderSearchRequest = {
    i_lang: 'EN',
    i_usercode: 'TESTUSER'
  };

  // Search results
  workOrders: WorkOrderItem[] = [];
  isLoading = false;
  error = '';
  hasSearched = false;

  // No additional state needed for simplified search

  constructor(private workOrderService: WorkOrderService) {}

  ngOnInit(): void {
    // No form data loading needed for simplified search
  }

  // No complex event handlers needed for simplified search

  searchWorkOrders(): void {
    this.isLoading = true;
    this.error = '';
    this.hasSearched = false;

    // Prepare the search request
    const request: WorkOrderSearchRequest = {
      ...this.searchCriteria
    };

    // Convert VIN to uppercase if provided
    if (request.vin && request.vin.trim().length > 0) {
      request.vin = request.vin.toUpperCase();
    }

    this.workOrderService.searchWorkOrders(request).subscribe({
      next: (response: any) => {
        if (response.success) {
          this.workOrders = response.work_orders || [];
          this.hasSearched = true;
        } else {
          this.error = response.message;
        }
        this.isLoading = false;
      },
      error: (error: any) => {
        this.error = 'Search failed: ' + error.message;
        this.isLoading = false;
      }
    });
  }

  clearSearch(): void {
    // Reset search criteria
    this.searchCriteria = {
      i_lang: 'EN',
      i_usercode: 'TESTUSER'
    };

    // No additional state to reset for simplified search

    // Clear results
    this.workOrders = [];
    this.hasSearched = false;
    this.error = '';
  }
}