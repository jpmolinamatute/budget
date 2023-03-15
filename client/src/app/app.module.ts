import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { MatRadioModule } from '@angular/material/radio';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import { PlanComponent } from './plan/plan.component';
import { BillComponent } from './bill/bill.component';
import { IncomeComponent } from './income/income.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

@NgModule({
  declarations: [AppComponent, PlanComponent, BillComponent, IncomeComponent],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    MatRadioModule,
    BrowserAnimationsModule,
  ],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}
