export function PageLoader() {
  return (
    <div className="flex min-h-[60vh] items-center justify-center" role="status">
      <div className="loader-spinner" />
      <span className="sr-only">Loading</span>
    </div>
  );
}
