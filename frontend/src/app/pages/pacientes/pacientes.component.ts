import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../core/api.service';
import { Paciente, PacientePayload } from '../../core/models';

@Component({
  selector: 'app-pacientes',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './pacientes.component.html',
  styleUrl: './pacientes.component.css',
})
export class PacientesComponent implements OnInit {
  pacientes: Paciente[] = [];
  filtro = '';
  showForm = false;
  editingId: number | null = null;
  error = '';
  success = '';

  form: PacientePayload = this.emptyForm();

  tiposSangre = ['O+', 'O-', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-'];

  constructor(private api: ApiService) {}

  ngOnInit(): void {
    this.load();
  }

  get filtrados(): Paciente[] {
    const q = this.filtro.trim().toLowerCase();
    if (!q) return this.pacientes;
    return this.pacientes.filter(
      (p) =>
        `${p.nombre} ${p.apellido}`.toLowerCase().includes(q) ||
        p.email.toLowerCase().includes(q) ||
        p.telefono.includes(q)
    );
  }

  emptyForm(): PacientePayload {
    return {
      nombre: '',
      apellido: '',
      fecha_nacimiento: '',
      telefono: '',
      email: '',
      direccion: '',
      tipo_sangre: 'O+',
    };
  }

  load(): void {
    this.api.getPacientes().subscribe({
      next: (data) => (this.pacientes = data),
      error: () => (this.error = 'Error al cargar pacientes.'),
    });
  }

  openCreate(): void {
    this.editingId = null;
    this.form = this.emptyForm();
    this.showForm = true;
    this.error = '';
    this.success = '';
  }

  openEdit(p: Paciente): void {
    this.editingId = p.id_paciente;
    this.form = {
      nombre: p.nombre,
      apellido: p.apellido,
      fecha_nacimiento: p.fecha_nacimiento,
      telefono: p.telefono,
      email: p.email,
      direccion: p.direccion,
      tipo_sangre: p.tipo_sangre,
    };
    this.showForm = true;
    this.error = '';
    this.success = '';
  }

  cancel(): void {
    this.showForm = false;
    this.editingId = null;
  }

  save(): void {
    const req =
      this.editingId == null
        ? this.api.createPaciente(this.form)
        : this.api.updatePaciente(this.editingId, this.form);

    req.subscribe({
      next: () => {
        this.success = this.editingId == null ? 'Paciente registrado.' : 'Paciente actualizado.';
        this.showForm = false;
        this.load();
      },
      error: (err) => {
        this.error = err?.error?.detail || 'No se pudo guardar el paciente.';
      },
    });
  }

  remove(p: Paciente): void {
    if (!confirm(`¿Eliminar a ${p.nombre} ${p.apellido}?`)) return;
    this.api.deletePaciente(p.id_paciente).subscribe({
      next: () => {
        this.success = 'Paciente eliminado.';
        this.load();
      },
      error: () => (this.error = 'No se pudo eliminar el paciente.'),
    });
  }
}
