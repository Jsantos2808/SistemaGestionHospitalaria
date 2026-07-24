import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { AuthService } from '../core/auth.service';

@Component({
  selector: 'app-shell',
  standalone: true,
  imports: [CommonModule, RouterOutlet, RouterLink, RouterLinkActive],
  templateUrl: './shell.component.html',
  styleUrl: './shell.component.css',
})
export class ShellComponent {
  user = this.auth.getUser();
  menuOpen = false;

  nav = [
    { path: '/app', label: 'Inicio', exact: true },
    { path: '/app/pacientes', label: 'Pacientes', exact: false },
    { path: '/app/citas', label: 'Citas', exact: false },
    { path: '/app/historial', label: 'Historial', exact: false },
  ];

  constructor(private auth: AuthService) {}

  logout(): void {
    this.auth.logout();
  }

  toggleMenu(): void {
    this.menuOpen = !this.menuOpen;
  }

  closeMenu(): void {
    this.menuOpen = false;
  }
}
