import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import {
  Cita,
  CitaPayload,
  DashboardStats,
  Historial,
  HistorialPayload,
  Medico,
  Paciente,
  PacientePayload,
} from './models';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private base = environment.apiUrl;

  constructor(private http: HttpClient) {}

  getStats(): Observable<DashboardStats> {
    return this.http.get<DashboardStats>(`${this.base}/dashboard/stats`);
  }

  getPacientes(): Observable<Paciente[]> {
    return this.http.get<Paciente[]>(`${this.base}/pacientes`);
  }

  createPaciente(payload: PacientePayload): Observable<Paciente> {
    return this.http.post<Paciente>(`${this.base}/pacientes`, payload);
  }

  updatePaciente(id: number, payload: PacientePayload): Observable<Paciente> {
    return this.http.put<Paciente>(`${this.base}/pacientes/${id}`, payload);
  }

  deletePaciente(id: number): Observable<{ ok: boolean }> {
    return this.http.delete<{ ok: boolean }>(`${this.base}/pacientes/${id}`);
  }

  getMedicos(): Observable<Medico[]> {
    return this.http.get<Medico[]>(`${this.base}/medicos`);
  }

  getCitas(): Observable<Cita[]> {
    return this.http.get<Cita[]>(`${this.base}/citas`);
  }

  createCita(payload: CitaPayload): Observable<Cita> {
    return this.http.post<Cita>(`${this.base}/citas`, payload);
  }

  updateCita(id: number, payload: Partial<CitaPayload>): Observable<Cita> {
    return this.http.put<Cita>(`${this.base}/citas/${id}`, payload);
  }

  deleteCita(id: number): Observable<{ ok: boolean }> {
    return this.http.delete<{ ok: boolean }>(`${this.base}/citas/${id}`);
  }

  getHistorial(idPaciente?: number): Observable<Historial[]> {
    let params = new HttpParams();
    if (idPaciente != null) {
      params = params.set('id_paciente', idPaciente);
    }
    return this.http.get<Historial[]>(`${this.base}/historial`, { params });
  }

  createHistorial(payload: HistorialPayload): Observable<Historial> {
    return this.http.post<Historial>(`${this.base}/historial`, payload);
  }

  updateHistorial(id: number, payload: Partial<HistorialPayload>): Observable<Historial> {
    return this.http.put<Historial>(`${this.base}/historial/${id}`, payload);
  }

  deleteHistorial(id: number): Observable<{ ok: boolean }> {
    return this.http.delete<{ ok: boolean }>(`${this.base}/historial/${id}`);
  }
}
