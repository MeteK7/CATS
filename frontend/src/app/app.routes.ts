import { Routes } from '@angular/router';
import { SapRecordList } from './components/sap-record-list/sap-record-list';
import { SapRecordForm } from './components/sap-record-form/sap-record-form';
import { WorkOrderSearchComponent } from './components/work-order-search/work-order-search';

export const routes: Routes = [
  { path: '', redirectTo: '/records', pathMatch: 'full' },
  { path: 'records', component: SapRecordList },
  { path: 'records/new', component: SapRecordForm },
  { path: 'records/:id/edit', component: SapRecordForm },
  { path: 'work-orders', component: WorkOrderSearchComponent },
  { path: '**', redirectTo: '/records' }
];
