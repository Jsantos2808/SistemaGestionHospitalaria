import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../core/api.service';
import { Historial, HistorialPayload, Medico, Paciente } from '../../core/models';

@Component({
  selector: 'app-historial',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './historial.component.html',
  styleUrl: './historial.component.css',
})
export class HistorialComponent implements OnInit {
  historiales: Historial[] = [];
  pacientes: Paciente[] = [];
  medicos: Medico[] = [];
  filtroPaciente: number | null = null;
  showForm = false;
  editingId: number | null = null;
  error = '';
  success = '';

  form: HistorialPayload = this.emptyForm();

  constructor(private api: ApiService) {}

  ngOnInit(): void {
    this.load();
    this.api.getPacientes().subscribe((p) => (this.pacientes = p));
    this.api.getMedicos().subscribe((m) => (this.medicos = m));
  }

  emptyForm(): HistorialPayload {
    return {
      id_paciente: 0,
      id_medico: 0,
      fecha_visita: new Date().toISOString().slice(0, 10),
      diagnostico: '',
      tratamiento: '',
      notas_adicionales: '',
    };
  }

  load(): void {
    this.api.getHistorial(this.filtroPaciente ?? undefined).subscribe({
      next: (data) => (this.historiales = data),
      error: () => (this.error = 'Error al cargar historial.'),
    });
  }

  onFilterChange(): void {
    this.load();
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

  openEdit(h: Historial): void {
    this.editingId = h.id_historial;
    this.form = {
      id_paciente: h.id_paciente,
      id_medico: h.id_medico,
      fecha_visita: h.fecha_visita,
      diagnostico: h.diagnostico,
      tratamiento: h.tratamiento,
      notas_adicionales: h.notas_adicionales || '',
    };
    this.showForm = true;
  }

  cancel(): void {
    this.showForm = false;
    this.editingId = null;
  }

  save(): void {
    const payload: HistorialPayload = {
      ...this.form,
      id_paciente: Number(this.form.id_paciente),
      id_medico: Number(this.form.id_medico),
    };

    const req =
      this.editingId == null
        ? this.api.createHistorial(payload)
        : this.api.updateHistorial(this.editingId, payload);

    req.subscribe({
      next: () => {
        this.success = this.editingId == null ? 'Historial registrado.' : 'Historial actualizado.';
        this.showForm = false;
        this.load();
      },
      error: (err) => {
        this.error = err?.error?.detail || 'No se pudo guardar el historial.';
      },
    });
  }

  remove(h: Historial): void {
    if (!confirm('¿Eliminar este registro de historial?')) return;
    this.api.deleteHistorial(h.id_historial).subscribe({
      next: () => {
        this.success = 'Historial eliminado.';
        this.load();
      },
      error: () => (this.error = 'No se pudo eliminar el historial.'),
    });
  }
}
