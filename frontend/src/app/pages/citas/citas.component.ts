import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../core/api.service';
import { Cita, CitaPayload, Medico, Paciente } from '../../core/models';

@Component({
  selector: 'app-citas',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './citas.component.html',
  styleUrl: './citas.component.css',
})
export class CitasComponent implements OnInit {
  citas: Cita[] = [];
  pacientes: Paciente[] = [];
  medicos: Medico[] = [];
  showForm = false;
  editingId: number | null = null;
  error = '';
  success = '';
  estados = ['Programada', 'Completada', 'Cancelada'];

  form: CitaPayload = this.emptyForm();

  constructor(private api: ApiService) {}

  ngOnInit(): void {
    this.load();
    this.api.getPacientes().subscribe((p) => (this.pacientes = p));
    this.api.getMedicos().subscribe((m) => (this.medicos = m));
  }

  emptyForm(): CitaPayload {
    return {
      id_paciente: 0,
      id_medico: 0,
      fecha_hora: '',
      motivo: '',
      estado: 'Programada',
    };
  }

  load(): void {
    this.api.getCitas().subscribe({
      next: (data) => (this.citas = data),
      error: () => (this.error = 'Error al cargar citas.'),
    });
  }

  openCreate(): void {
    this.editingId = null;
    this.form = this.emptyForm();
    if (this.pacientes[0]) this.form.id_paciente = this.pacientes[0].id_paciente;
    if (this.medicos[0]) this.form.id_medico = this.medicos[0].id_medico;
    this.showForm = true;
    this.error = '';
    this.success = '';
  }

  openEdit(c: Cita): void {
    this.editingId = c.id_cita;
    this.form = {
      id_paciente: c.id_paciente,
      id_medico: c.id_medico,
      fecha_hora: c.fecha_hora.slice(0, 16),
      motivo: c.motivo,
      estado: c.estado,
    };
    this.showForm = true;
  }

  cancel(): void {
    this.showForm = false;
    this.editingId = null;
  }

  toIsoLocal(value: string): string {
    // datetime-local -> ISO without timezone for FastAPI
    if (!value) return value;
    return value.length === 16 ? `${value}:00` : value;
  }

  save(): void {
    const payload: CitaPayload = {
      ...this.form,
      id_paciente: Number(this.form.id_paciente),
      id_medico: Number(this.form.id_medico),
      fecha_hora: this.toIsoLocal(this.form.fecha_hora),
    };

    const req =
      this.editingId == null
        ? this.api.createCita(payload)
        : this.api.updateCita(this.editingId, payload);

    req.subscribe({
      next: () => {
        this.success = this.editingId == null ? 'Cita creada.' : 'Cita actualizada.';
        this.showForm = false;
        this.load();
      },
      error: (err) => {
        this.error = err?.error?.detail || 'No se pudo guardar la cita.';
      },
    });
  }

  setEstado(c: Cita, estado: string): void {
    this.api.updateCita(c.id_cita, { estado }).subscribe({
      next: () => this.load(),
      error: () => (this.error = 'No se pudo actualizar el estado.'),
    });
  }

  remove(c: Cita): void {
    if (!confirm('¿Eliminar esta cita?')) return;
    this.api.deleteCita(c.id_cita).subscribe({
      next: () => {
        this.success = 'Cita eliminada.';
        this.load();
      },
      error: () => (this.error = 'No se pudo eliminar la cita.'),
    });
  }

  statusClass(estado: string): string {
    if (estado === 'Completada') return 'ok';
    if (estado === 'Cancelada') return 'bad';
    return 'warn';
  }
}
