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
  wo_type?: string;
  wo_type_multi?: string;
  wo_status?: string;
  wo_status_multi?: string;
  fg_status_multi?: string;
  country?: string;
  wonay?: string;
  ra_country?: string;
  vin?: string;
  ostrateji_td?: string;
  ostrateji_tg?: string;
  ostrateji_ti?: string;
  ostrateji_tf?: string;
  ostrateji_tx?: string;
  ostrateji_ty?: string;
  ostrateji_tz?: string;
  ostrateji_tu?: string;
  zcats_wo_conv?: string;
  creuser?: string;
  zgos?: string;
  demo?: string;
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
  wo_types: DropdownOption[];
  wo_statuses: DropdownOption[];
  fg_statuses: DropdownOption[];
  countries: DropdownOption[];
  approval_statuses: DropdownOption[];
  ra_countries: DropdownOption[];
  strategies: DropdownOption[];
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
  formData: SearchFormData = {
    wo_types: [],
    wo_statuses: [],
    fg_statuses: [],
    countries: [],
    approval_statuses: [],
    ra_countries: [],
    strategies: []
  };

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

  // Multi-select arrays
  selectedWoTypes: string[] = [];
  selectedWoStatuses: string[] = [];
  selectedFgStatuses: string[] = [];

  // Checkbox states
  convertCheck = false;
  onlyLoginUser = false;
  egyptSelected = false;
  demoSelected = false;

  constructor(private workOrderService: WorkOrderService) {}

  ngOnInit(): void {
    this.loadFormData();
  }

  loadFormData(): void {
    this.isLoading = true;
    this.workOrderService.getFormData().subscribe({
      next: (data: SearchFormData) => {
        this.formData = data;
        this.isLoading = false;
      },
      error: (error: any) => {
        this.error = 'Failed to load form data: ' + error.message;
        this.isLoading = false;
      }
    });
  }

  onWoTypeChange(event: any): void {
    const value = event.target.value;
    const checked = event.target.checked;
    
    if (checked) {
      this.selectedWoTypes.push(value);
    } else {
      const index = this.selectedWoTypes.indexOf(value);
      if (index > -1) {
        this.selectedWoTypes.splice(index, 1);
      }
    }
  }

  onWoStatusChange(event: any): void {
    const value = event.target.value;
    const checked = event.target.checked;
    
    if (checked) {
      this.selectedWoStatuses.push(value);
    } else {
      const index = this.selectedWoStatuses.indexOf(value);
      if (index > -1) {
        this.selectedWoStatuses.splice(index, 1);
      }
    }
  }

  onFgStatusChange(event: any): void {
    const value = event.target.value;
    const checked = event.target.checked;
    
    if (checked) {
      this.selectedFgStatuses.push(value);
    } else {
      const index = this.selectedFgStatuses.indexOf(value);
      if (index > -1) {
        this.selectedFgStatuses.splice(index, 1);
      }
    }
  }

  onStrategyChange(strategy: string): void {
    // Clear all strategy flags first
    this.searchCriteria.ostrateji_td = undefined;
    this.searchCriteria.ostrateji_tg = undefined;
    this.searchCriteria.ostrateji_ti = undefined;
    this.searchCriteria.ostrateji_tf = undefined;
    this.searchCriteria.ostrateji_tx = undefined;
    this.searchCriteria.ostrateji_ty = undefined;
    this.searchCriteria.ostrateji_tz = undefined;
    this.searchCriteria.ostrateji_tu = undefined;

    // Set the selected strategy flag
    if (strategy === 'TG') this.searchCriteria.ostrateji_tg = 'X';
    else if (strategy === 'TI') this.searchCriteria.ostrateji_ti = 'X';
    else if (strategy === 'TD') this.searchCriteria.ostrateji_td = 'X';
    else if (strategy === 'TF') this.searchCriteria.ostrateji_tf = 'X';
    else if (strategy === 'TU') this.searchCriteria.ostrateji_tu = 'X';
    else if (strategy === 'TX') this.searchCriteria.ostrateji_tx = 'X';
    else if (strategy === 'TY') this.searchCriteria.ostrateji_ty = 'X';
    else if (strategy === 'TZ') this.searchCriteria.ostrateji_tz = 'X';
  }

  searchWorkOrders(): void {
    this.isLoading = true;
    this.error = '';
    this.hasSearched = false;

    // Prepare the search request
    const request: WorkOrderSearchRequest = {
      ...this.searchCriteria,
      wo_type_multi: this.selectedWoTypes.join(','),
      wo_status_multi: this.selectedWoStatuses.join(','),
      fg_status_multi: this.selectedFgStatuses.join(','),
      zcats_wo_conv: this.convertCheck ? 'X' : '',
      creuser: this.onlyLoginUser ? this.searchCriteria.i_usercode : '',
      zgos: this.egyptSelected ? 'X' : '',
      demo: this.demoSelected ? 'X' : ''
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

    // Reset multi-select arrays
    this.selectedWoTypes = [];
    this.selectedWoStatuses = [];
    this.selectedFgStatuses = [];

    // Reset checkboxes
    this.convertCheck = false;
    this.onlyLoginUser = false;
    this.egyptSelected = false;
    this.demoSelected = false;

    // Clear results
    this.workOrders = [];
    this.hasSearched = false;
    this.error = '';
  }
}