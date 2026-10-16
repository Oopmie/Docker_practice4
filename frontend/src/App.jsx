import React, { useState } from 'react';
import styles from './UserForm.module.scss';

const UserForm = () => {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    // Шаг 1: Публичный профиль
    lastName: '',
    firstName: '',
    middleName: '',
    mobilePhone: '',
    homePhone: '',
    birthDate: '',
    gender: 'Мужской',
    email: '',
    
    // Шаг 2: Приватный паспорт
    passportSeriesNumber: '',
    passportIssueDate: '',
    departmentCode: '',
    issuedBy: '',
    birthAddress: '',
    actualAddress: '',
    hasInternationalPassport: false,
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const handleNext = (e) => {
    e.preventDefault();
    // Простая валидация для первого шага
    if (!formData.lastName || !formData.firstName || !formData.mobilePhone || !formData.birthDate || !formData.email) {
      alert('Пожалуйста, заполните все обязательные поля.');
      return;
    }
    setStep(2);
  };

  const handleBack = () => setStep(1);

    const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      // Отправляем данные на наш созданный Python бэкенд
      const response = await fetch('http://localhost:8000/api/save-profile', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      const result = await response.json();

      if (response.ok) {
        alert('🎉 Данные успешно сохранены в базу данных PostgreSQL!');
        // Тут можно очистить форму, если нужно
      } else {
        alert(`Ошибка сервера: ${result.detail}`);
      }
    } catch (error) {
      console.error('Ошибка отправки:', error);
      alert('Не удалось связаться с сервером бэкенда.');
    }
  };


  return (
    <div className={styles.formContainer}>
      <div className={styles.progressbar}>
        <div className={`${styles.progressStep} ${step >= 1 ? styles.active : ''}`}>1. Профиль</div>
        <div className={`${styles.progressStep} ${step === 2 ? styles.active : ''}`}>2. Паспортные данные</div>
      </div>

      <form onSubmit={step === 1 ? handleNext : handleSubmit} className={styles.form}>
        {step === 1 && (
          <div className={styles.stepBlock}>
            <h2>Общая информация (Доступно всем)</h2>
            
            <div className={styles.inputGroup}>
              <label>Фамилия *</label>
              <input type="text" name="lastName" value={formData.lastName} onChange={handleChange} required />
            </div>

            <div className={styles.inputGroup}>
              <label>Имя *</label>
              <input type="text" name="firstName" value={formData.firstName} onChange={handleChange} required />
            </div>

            <div className={styles.inputGroup}>
              <label>Отчество</label>
              <input type="text" name="middleName" value={formData.middleName} onChange={handleChange} />
            </div>

            <div className={styles.row}>
              <div className={styles.inputGroup}>
                <label>Мобильный телефон *</label>
                <input type="tel" name="mobilePhone" placeholder="+7 (999) 999-99-99" value={formData.mobilePhone} onChange={handleChange} required />
              </div>
              <div className={styles.inputGroup}>
                <label>Домашний телефон</label>
                <input type="tel" name="homePhone" value={formData.homePhone} onChange={handleChange} />
              </div>
            </div>

            <div className={styles.row}>
              <div className={styles.inputGroup}>
                <label>Дата рождения *</label>
                <input type="date" name="birthDate" value={formData.birthDate} onChange={handleChange} required />
              </div>
              <div className={styles.inputGroup}>
                <label>Пол *</label>
                <select name="gender" value={formData.gender} onChange={handleChange}>
                  <option value="Мужской">Мужской</option>
                  <option value="Женский">Женский</option>
                </select>
              </div>
            </div>

            <div className={styles.inputGroup}>
              <label>Email *</label>
              <input type="email" name="email" placeholder="example@mail.com" value={formData.email} onChange={handleChange} required />
            </div>

            <button type="submit" className={styles.btnPrimary}>Далее</button>
          </div>
        )}

        {step === 2 && (
          <div className={styles.stepBlock}>
            <h2>Конфиденциальные данные (Ограниченный доступ)</h2>

            <div className={styles.row}>
              <div className={styles.inputGroup}>
                <label>Серия и номер паспорта *</label>
                <input type="text" name="passportSeriesNumber" placeholder="45 12 123456" value={formData.passportSeriesNumber} onChange={handleChange} required />
              </div>
              <div className={styles.inputGroup}>
                <label>Код подразделения *</label>
                <input type="text" name="departmentCode" placeholder="770-001" value={formData.departmentCode} onChange={handleChange} required />
              </div>
            </div>

            <div className={styles.row}>
              <div className={styles.inputGroup}>
                <label>Дата выдачи паспорта *</label>
                <input type="date" name="passportIssueDate" value={formData.passportIssueDate} onChange={handleChange} required />
              </div>
            </div>

            <div className={styles.inputGroup}>
              <label>Кем выдан паспорт *</label>
              <textarea name="issuedBy" rows="2" value={formData.issuedBy} onChange={handleChange} required />
            </div>

            <div className={styles.inputGroup}>
              <label>Адрес рождения *</label>
              <input type="text" name="birthAddress" value={formData.birthAddress} onChange={handleChange} required />
            </div>

            <div className={styles.inputGroup}>
              <label>Адрес фактического проживания *</label>
              <input type="text" name="actualAddress" value={formData.actualAddress} onChange={handleChange} required />
            </div>

            <div className={styles.checkboxGroup}>
              <input type="checkbox" id="hasInt" name="hasInternationalPassport" checked={formData.hasInternationalPassport} onChange={handleChange} />
              <label htmlFor="hasInt">Есть загранпаспорт</label>
            </div>

            <div className={styles.btnRow}>
              <button type="button" onClick={handleBack} className={styles.btnSecondary}>Назад</button>
              <button type="submit" className={styles.btnSuccess}>Сохранить данные</button>
            </div>
          </div>
        )}
      </form>
    </div>
  );
};

export default UserForm;