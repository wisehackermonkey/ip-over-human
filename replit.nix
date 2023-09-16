{ pkgs }: {
  deps = [
    pkgs.python37
    pkgs.nodePackages.vscode-langservers-extracted
    pkgs.nodePackages.typescript-language-server  
  ];
}