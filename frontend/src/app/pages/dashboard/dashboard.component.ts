import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { ApiService } from '../../core/api.service';
import { AuthService } from '../../core/auth.service';
import { Cita, DashboardStats } from '../../core/models';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css',
})
export class DashboardComponent implements OnInit {
  user = this.auth.getUser();
  stats: DashboardStats | null = null;
  proximas: Cita[] = [];
  error = '';

  constructor(private api: ApiService, private auth: AuthService) {}

  ngOnInit(): void {
    this.api.getStats().subscribe({
      next: (s) => (this.stats = s),
      error: () => (this.error = 'No se pudieron cargar las estadísticas.'),
    });
    this.api.getCitas().subscribe({
      next: (citas) => {
        this.proximas = citas
          .filter((c) => c.estado === 'Programada')
          .slice(0, 5);
      },
    });
  }
}
