export default function ErrorBanner({ error }: { error: unknown }) {
  const message = error instanceof Error ? error.message : "Something went wrong";
  return <div className="error-banner" role="alert">{message}</div>;
}
