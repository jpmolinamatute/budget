import { Component } from '@angular/core';

@Component({
  selector: 'app-income',
  templateUrl: './income.component.html',
  styleUrls: ['./income.component.scss'],
})
export class IncomeComponent {
  income_array = [
    {
      id: '35b93c12-47cf-4219-8f40-c05ddba9a665',
      date: '2023-02-01',
      amount: 5.18,
      income_type: 'other',
      budget_id: '4849cb99-b084-4024-b613-8f3e0cd1079c',
      plan_id: '7a698a7d-9d77-4106-aabb-1e9ade024812',
      is_locked: false,
    },
    {
      id: '02c19a7f-ad0d-4e49-a8b6-2cf0e0fabe06',
      date: '2023-02-03',
      amount: 2920.92,
      income_type: 'salary',
      budget_id: '4849cb99-b084-4024-b613-8f3e0cd1079c',
      plan_id: '7a698a7d-9d77-4106-aabb-1e9ade024812',
      is_locked: true,
    },
    {
      id: '6ac073f2-e40d-4ef7-8fd2-0178c0f48d53',
      date: '2023-02-17',
      amount: 2920.92,
      income_type: 'salary',
      budget_id: '4849cb99-b084-4024-b613-8f3e0cd1079c',
      plan_id: 'b3708541-388d-45cf-8abe-6a69f15c7537',
      is_locked: false,
    },
  ];
}
