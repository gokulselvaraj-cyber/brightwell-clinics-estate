CREATE TABLE bw.visit_summary (
    summary_id    uuid PRIMARY KEY,
    visit_id      bigint NOT NULL REFERENCES bw.visit (id),
    status        varchar(10) NOT NULL DEFAULT 'DRAFT' CHECK (status IN ('DRAFT', 'SIGNED', 'REJECTED')),
    summary_text  text NOT NULL,
    model_version varchar(40),
    requested_by  varchar(64) NOT NULL,
    created_at    timestamptz NOT NULL DEFAULT now(),
    signed_at     timestamptz
);
COMMENT ON TABLE bw.visit_summary IS 'AI-drafted visit summaries; health data. Retention 2 years (V7).';
CREATE INDEX ix_visit_summary_visit ON bw.visit_summary (visit_id);
