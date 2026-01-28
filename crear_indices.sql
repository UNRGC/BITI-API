-- ============================================
-- FASE 2: CREACIÓN DE ÍNDICES
-- ============================================
USE bdBiti;
GO

-- Índice por fecha
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Registros_Fecha' AND object_id = OBJECT_ID('registros'))
BEGIN
    CREATE INDEX IX_Registros_Fecha ON registros(fecha DESC);
    PRINT '✅ Índice IX_Registros_Fecha creado';
END
GO

-- Índice por cliente
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Registros_Cliente' AND object_id = OBJECT_ID('registros'))
BEGIN
    CREATE INDEX IX_Registros_Cliente ON registros(cliente);
    PRINT '✅ Índice IX_Registros_Cliente creado';
END
GO

-- Índice por empresa
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Registros_Empresa' AND object_id = OBJECT_ID('registros'))
BEGIN
    CREATE INDEX IX_Registros_Empresa ON registros(empresa);
    PRINT '✅ Índice IX_Registros_Empresa creado';
END
GO

-- Índice por póliza
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Registros_Poliza' AND object_id = OBJECT_ID('registros'))
BEGIN
    CREATE INDEX IX_Registros_Poliza ON registros(poliza);
    PRINT '✅ Índice IX_Registros_Poliza creado';
END
GO

-- Índice por monto
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Registros_Monto' AND object_id = OBJECT_ID('registros'))
BEGIN
    CREATE INDEX IX_Registros_Monto ON registros(monto DESC);
    PRINT '✅ Índice IX_Registros_Monto creado';
END
GO

-- Índice compuesto cliente + fecha
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Registros_Cliente_Fecha' AND object_id = OBJECT_ID('registros'))
BEGIN
    CREATE INDEX IX_Registros_Cliente_Fecha ON registros(cliente, fecha DESC);
    PRINT '✅ Índice IX_Registros_Cliente_Fecha creado';
END
GO

-- Índice compuesto empresa + fecha
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Registros_Empresa_Fecha' AND object_id = OBJECT_ID('registros'))
BEGIN
    CREATE INDEX IX_Registros_Empresa_Fecha ON registros(empresa, fecha DESC);
    PRINT '✅ Índice IX_Registros_Empresa_Fecha creado';
END
GO

-- Índice compuesto para dashboard
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Registros_Dashboard' AND object_id = OBJECT_ID('registros'))
BEGIN
    CREATE NONCLUSTERED INDEX IX_Registros_Dashboard
    ON registros(fecha DESC)
    INCLUDE (monto, cliente, empresa, poliza);
    PRINT '✅ Índice IX_Registros_Dashboard creado';
END
GO

PRINT '';
PRINT '================================================';
PRINT '✅ Todos los índices creados exitosamente';
PRINT '================================================';
GO