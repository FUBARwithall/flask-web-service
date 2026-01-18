-- Migration: Add notes column to face_analyses and body_analyses tables
-- Date: 2026-01-17

-- Add notes column to face_analyses
ALTER TABLE face_analyses ADD COLUMN notes TEXT;

-- Add notes column to body_analyses
ALTER TABLE body_analyses ADD COLUMN notes TEXT;
